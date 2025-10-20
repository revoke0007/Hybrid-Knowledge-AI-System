from pinecone import Pinecone
import config

try:
    pc = Pinecone(api_key=config.PINECONE_API_KEY)
    indexes = pc.list_indexes()
    print("Connected to Pinecone!")
    print("Available indexes:", indexes)
except Exception as e:
    print("Connection failed:", e)
