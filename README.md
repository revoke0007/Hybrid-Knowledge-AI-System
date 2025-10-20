
# Hybrid Knowledge AI System

A hybrid retrieval and reasoning pipeline that combines **vector similarity search (Pinecone)**, **graph-based reasoning (Neo4j)**, and **OpenAI GPT** to provide **context-aware, intelligent answers** about travel destinations.

This project demonstrates how to integrate structured graph databases and unstructured embeddings into one conversational AI assistant.

***

## 🧠 Overview

This system builds a **travel recommendation assistant** using three knowledge layers:

- **Neo4j:** for graph-based relationships (e.g., cities, attractions, and connections).
- **Pinecone:** for semantic similarity search using OpenAI embeddings.
- **OpenAI GPT model:** for natural language understanding and reasoning.

Together, they provide intelligent responses that combine vector semantics and relationship-based insights.

***

## ⚙️ Architecture

| Component | Description |
| :-- | :-- |
| `load_to_neo4j.py` | Loads travel data (JSON) into Neo4j, creating nodes and relationships. |
| `visualize_graph.py` | Visualizes the loaded Neo4j knowledge graph using PyVis and NetworkX. |
| `pinecone_upload.py` | Generates OpenAI embeddings for each data item and uploads vectors to Pinecone. |
| `hybrid_chat.py` | A hybrid chatbot that queries both Pinecone and Neo4j, then reasons with OpenAI GPT. |
| `config.py` | Contains credentials and environment configurations for APIs and databases. |


***

## 📥 Installation

1. **Clone the Repository**

```bash
git clone https://github.com/revoke0007/hybrid-knowledge-ai-system.git
cd hybrid-knowledge-ai-system
```

2. **Create and Activate Python Environment**

```bash
python -m venv venv
venv\Scripts\activate       # For Windows
```

3. **Install Dependencies**

```bash
pip install openai pinecone-client tqdm neo4j networkx pyvis
```

4. **Setup Configuration**
    - Copy `config.py`
    - Fill in your credentials:

```python
OPENAI_API_KEY = "sk-..."        # From https://platform.openai.com/api-keys,, (my key in config folder)
PINECONE_API_KEY = "pcsk-..."    # From https://www.pinecone.io,, (my key in config folder)
NEO4J_URI = "bolt://localhost:7687"
NEO4J_USER = "neo4j"
NEO4J_PASSWORD = "password"
```


***

## 🗃️ Data Loading Steps

1. **Load Graph Data Into Neo4j**

```bash
python load_to_neo4j.py
<img width="714" height="712" alt="Load graph data ss" src="https://github.com/user-attachments/assets/522ce8f9-b7c9-4230-829b-1f8d7e9899ef" />

<img width="1043" height="716" alt="Load graph data ss" src="https://github.com/user-attachments/assets/128f7d87-415a-44ed-a665-091db9dfb4de" />

```

2. **Visualize Graph (Optional)**

```bash
python visualize_graph.py
```

→ Opens interactive graph HTML file (`neo4j_viz.html`)
3. **Upload Vectors to Pinecone**

```bash
python pinecone_upload.py

<img width="824" height="542" alt="upload complete vector to pinecone" src="https://github.com/user-attachments/assets/25e12c57-8d73-49d2-b524-fc2fabb311c9" />

```

→ Embeds and uploads semantic vectors from dataset JSON

***

## 💬 Run the Hybrid Chat Assistant

Start your chatbot:

```bash
python hybrid_chat.py

<img width="1268" height="714" alt="final output/answer" src="https://github.com/user-attachments/assets/c832d123-7dc6-47b7-b000-9f386b0df78a" />

```

Example query:

```
Enter your travel question: What are the top attractions in Hanoi?
```

The system retrieves related nodes (from Neo4j), ranks similar embeddings (from Pinecone), and composes an answer using GPT.

***

## 🧩 Technology Stack

| Layer | Technology Used |
| :-- | :-- |
| Vector DB | Pinecone |
| Graph DB | Neo4j |
| LLM API | OpenAI GPT‑4o mini |
| Backend | Python 3.10+ |
| Libraries | `openai`, `pinecone-client`, `neo4j`, `networkx`, `pyvis`, `tqdm` |


***

## 🏗️ Project Flow

1. **Dataset Preparation:** Provide JSON dataset (`vietnam_travel_dataset.json`) including IDs, names, descriptions, and relations.
2. **Graph Creation:** Load and link nodes in Neo4j.
3. **Semantic Indexing:** Create embeddings and store in Pinecone.
4. **Query Execution:** User queries → Embedding search + graph context + GPT response.

***

## 🚀 Demo Output

```
Hybrid travel assistant. Type 'exit' to quit.

Enter your travel question: What are must‑visit places in Hanoi?
DEBUG: Pinecone top 5 results: 5
DEBUG: Graph facts: 12

=== Assistant Answer ===
You can visit Hoan Kiem Lake (id‑lake_hoankiem), Temple of Literature (id‑temple_lit), and Old Quarter (id‑oldquarter).
These are culturally significant and close to city center.
=== End ===
```


***

## 🧰 Folder Structure

```
├── config.py
├── test_pinecone_connection.py
├── test_neo4j_connection.py
├── load_to_neo4j.py
├── pinecone_upload.py
├── visualize_graph.py
├── hybrid_chat.py
├── vietnam_travel_dataset.json
├── improvement.md
├── project_explaination.md
└── README.md
```


***

## 🧾 Requirements

Create a `requirements.txt` file:

```
openai
pinecone-client
neo4j
tqdm
networkx
pyvis
```


***

## 🤝 Contributing

Pull requests are welcome!
If you'd like to improve this project, fork the repo and submit your enhancements.

***


## 👨‍💻 Author

Created by **[Hardeep Rohilla]**

- GitHub: [@revoke0007](https://github.com/revoke0007)
- Email: hardeeprohilla65@gmail.com

***


