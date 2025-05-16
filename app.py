from neo4j import GraphDatabase
from dotenv import load_dotenv
import os

# Load env vars from .env file
load_dotenv()

# Read the variables
URI = os.getenv("NEO4J_URI")
USER = os.getenv("NEO4J_USER")
PASSWORD = os.getenv("NEO4J_PASSWORD")




# URI examples: "neo4j://localhost", "neo4j+s://xxx.databases.neo4j.io"

AUTH = (USER,PASSWORD )

with GraphDatabase.driver(URI, auth=AUTH) as driver:
    driver.verify_connectivity()


from neo4j import GraphDatabase

class MedicalKG:
    def __init__(self, uri, user, password):
        self.driver = GraphDatabase.driver(uri, auth=(user, password))
        
    def close(self):
        self.driver.close()
        
    def get_diseases_by_symptoms(self, symptoms):
        with self.driver.session() as session:
            query = """
            MATCH (s:Symptom)-[:INDICATES]->(d:Disease)
            WHERE s.name IN $symptoms
            RETURN d.name AS disease, count(*) AS match_count
            ORDER BY match_count DESC
            """
            result = session.run(query, symptoms=symptoms)
            return [record["disease"] for record in result]

# Usage
kg = MedicalKG("bolt://localhost:7687", "neo4j", "medicaldata")
diseases = kg.get_diseases_by_symptoms(["Fever", "Joint Pain"])
print("Possible diseases:", diseases)
kg.close()
