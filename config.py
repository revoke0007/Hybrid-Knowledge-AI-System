# config_example.py — copy to config.py and fill with real values.
NEO4J_URI = "bolt://localhost:7687"
NEO4J_USER = "neo4j"
NEO4J_PASSWORD = "password"

OPENAI_API_KEY = "sk proj-mJGI" # this key is wrong for security reason

PINECONE_API_KEY = "pcsk6_5rbMk4" # wrong key
PINECONE_ENV = "us-east-1"   # example
PINECONE_INDEX_NAME = "vietnam-travels"
PINECONE_VECTOR_DIM = 1536       # adjust to embedding model used (text-embedding-3-large ~ 3072? check your model); we assume 1536 for common OpenAI models — change if needed.
