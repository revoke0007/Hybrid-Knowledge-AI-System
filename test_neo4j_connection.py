# test_neo4j_connection.py
from neo4j import GraphDatabase
import config

def test_connection():
    driver = GraphDatabase.driver(config.NEO4J_URI, auth=(config.NEO4J_USER, config.NEO4J_PASSWORD))
    try:
        with driver.session() as session:
            r = session.run("RETURN 'Connected to Neo4j!' AS message")
            for rec in r:
                print(rec["message"])
        print("Connection successful!")
    except Exception as e:
        print("Connection failed:", e)
    finally:
        driver.close()

if __name__ == "__main__":
    test_connection()
