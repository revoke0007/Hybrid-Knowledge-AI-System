import json
from typing import List
from openai import OpenAI
from pinecone import Pinecone, ServerlessSpec
from neo4j import GraphDatabase
import config

# -----------------------------
# Config
# -----------------------------
EMBED_MODEL = "text-embedding-3-small"
CHAT_MODEL = "gpt-4o-mini"
TOP_K = 5

INDEX_NAME = config.PINECONE_INDEX_NAME

# -----------------------------
# Initialize clients
# -----------------------------
client = OpenAI(api_key=config.OPENAI_API_KEY)
pc = Pinecone(api_key=config.PINECONE_API_KEY)

# -----------------------------
# Pinecone index initialization 
# -----------------------------
existing_indexes = pc.list_indexes().names()
if INDEX_NAME not in existing_indexes:
    print(f"Creating managed index: {INDEX_NAME}")
    pc.create_index(
        name=INDEX_NAME,
        dimension=config.PINECONE_VECTOR_DIM,
        metric="cosine",
        spec=ServerlessSpec(
            cloud="gcp",          # Make sure this matches your index's cloud provider
            region="us-east1-gcp"
        )
    )
else:
    print(f"Index {INDEX_NAME} already exists.")

index = pc.Index(INDEX_NAME)

# -----------------------------
# Neo4j connection
# -----------------------------
driver = GraphDatabase.driver(
    config.NEO4J_URI, auth=(config.NEO4J_USER, config.NEO4J_PASSWORD)
)

# -----------------------------
# Embedding cache
# -----------------------------
embedding_cache = {}

def cached_embed_text(text: str) -> List[float]:
    if text in embedding_cache:
        return embedding_cache[text]
    try:
        resp = client.embeddings.create(model=EMBED_MODEL, input=[text])
        embedding = resp.data[0].embedding
        embedding_cache[text] = embedding
        return embedding
    except Exception as e:
        print(f"Embedding API error: {e}")
        return []

# -----------------------------
# Pinecone query function
# -----------------------------
def pinecone_query(query_text: str, top_k=TOP_K):
    vec = cached_embed_text(query_text)
    if not vec:
        print("Failed to get embedding for query.")
        return []
    try:
        res = index.query(
            vector=vec,
            top_k=top_k,
            include_metadata=True,
            include_values=False
        )
        print(f"DEBUG: Pinecone returned {len(res['matches'])} matches")
        return res["matches"]
    except Exception as e:
        print(f"Pinecone query error: {e}")
        return []

# -----------------------------
# Fetch Neo4j neighborhood facts
# -----------------------------
def fetch_graph_context(node_ids: List[str], neighborhood_depth=1):
    facts = []
    with driver.session() as session:
        for nid in node_ids:
            try:
                q = (
                    "MATCH (n:Entity {id:$nid})-[r]-(m:Entity) "
                    "RETURN type(r) AS rel, labels(m) AS labels, m.id AS id, "
                    "m.name AS name, m.type AS type, m.description AS description "
                    "LIMIT 10"
                )
                recs = session.run(q, nid=nid)
                for r in recs:
                    facts.append({
                        "source": nid,
                        "rel": r["rel"],
                        "target_id": r["id"],
                        "target_name": r["name"],
                        "target_desc": (r["description"] or "")[:400],
                        "labels": r["labels"]
                    })
            except Exception as e:
                print(f"Neo4j query error for node {nid}: {e}")
    print(f"DEBUG: Graph facts fetched: {len(facts)}")
    return facts

# -----------------------------
# Helper: Summarize top Pinecone matches
# -----------------------------
def search_summary(matches):
    summary = []
    for m in matches[:3]:
        meta = m.get("metadata", {})
        name = meta.get("name", "Unknown")
        type_ = meta.get("type", "Entity")
        city = meta.get("city", "Unknown")
        summary.append(f"{name} ({type_}) in {city}")
    return ", ".join(summary)

# -----------------------------
# Build prompt for GPT model
# -----------------------------
def build_prompt(user_query, pinecone_matches, graph_facts):
    system = (
        "You are a helpful travel assistant. Use the provided semantic search results "
        "and graph facts to answer the user's query briefly and concisely. "
        "If needed, think step-by-step and cite node ids when referencing specific places or attractions. "
        "Suggest 2–3 actionable itinerary steps or tips."
    )

    summary_text = search_summary(pinecone_matches)

    vec_context = [
        f"- id: {m['id']}, name: {m['metadata'].get('name','')}, score: {m.get('score')}"
        for m in pinecone_matches[:10]
    ]

    graph_context = [
        f"- ({f['source']}) -[{f['rel']}]-> ({f['target_id']}) {f['target_name']}: {f['target_desc']}"
        for f in graph_facts[:20]
    ]

    prompt = [
        {"role": "system", "content": system},
        {"role": "user", "content":
         f"User query: {user_query}\n\n"
         f"Summary of top matches: {summary_text}\n\n"
         "Details of semantic matches:\n" + "\n".join(vec_context) + "\n\n"
         "Graph facts (neighboring relations):\n" + "\n".join(graph_context) + "\n\n"
         "Based on the above, answer the user's question."}
    ]
    return prompt

# -----------------------------
# Call GPT chat completion
# -----------------------------
def call_chat(prompt_messages):
    try:
        resp = client.chat.completions.create(
            model=CHAT_MODEL,
            messages=prompt_messages,
            max_tokens=600,
            temperature=0.2
        )
        return resp.choices[0].message.content
    except Exception as e:
        return f"OpenAI Chat API error: {e}"

# -----------------------------
# Interactive chat loop
# -----------------------------
def interactive_chat():
    print("Hybrid travel assistant. Type 'exit' or 'quit' to stop.")
    while True:
        try:
            query = input("\nEnter your travel question: ").strip()
            if not query or query.lower() in ("exit", "quit"):
                print("Goodbye!")
                break

            matches = pinecone_query(query, top_k=TOP_K)
            if not matches:
                print("No semantic matches found. Please try a different query.")
                continue

            match_ids = [m["id"] for m in matches]
            graph_facts = fetch_graph_context(match_ids)

            prompt = build_prompt(query, matches, graph_facts)
            answer = call_chat(prompt)

            print("\n=== Assistant Answer ===\n")
            print(answer)
            print("\n=== End ===\n")

        except KeyboardInterrupt:
            print("\nInterrupted! Exiting.")
            break
        except Exception as e:
            print(f"Unexpected error: {e}")

if __name__ == "__main__":
    interactive_chat()
