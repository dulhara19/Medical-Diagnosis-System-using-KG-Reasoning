from neo4j import GraphDatabase
from dotenv import load_dotenv
import os

# Load env vars from .env file
load_dotenv()

# Read the variables
URI = os.getenv("NEO4J_URI")
USER = os.getenv("NEO4J_USER")
PASSWORD = os.getenv("NEO4J_PASSWORD")

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
             WITH d, count(s) AS matchedSymptoms
            MATCH (d)<-[:INDICATES]-(allSymptoms:Symptom)
            WITH d.name AS disease, matchedSymptoms, count(allSymptoms) AS totalSymptoms
            RETURN disease, matchedSymptoms, totalSymptoms,
               toFloat(matchedSymptoms) / totalSymptoms AS confidence
            ORDER BY confidence DESC
            """
            result = session.run(query, symptoms=symptoms)
            return [
                {
                    "disease": record["disease"],
                    "confidence": round(record["confidence"] * 100, 2),  # in %
                    "matched": record["matchedSymptoms"],
                    "total": record["totalSymptoms"]
                 }
            for record in result
                ]

        
    def get_treatments_by_disease(self, disease):
        with self.driver.session() as session:
            query = """
            MATCH (d:Disease {name: $disease})-[:TREATED_BY]->(drug:Drug)
            RETURN drug.name AS drug
            """
            result = session.run(query, disease=disease)
            return [record["drug"] for record in result]

    def get_tests_by_disease(self, disease):
        with self.driver.session() as session:
            query = """
            MATCH (d:Disease {name: $disease})-[:REQUIRES_TEST]->(test:Test)
            RETURN test.name AS test
            """
            result = session.run(query, disease=disease)
            return [record["test"] for record in result]
    

# Usage
kg = MedicalKG(URI, USER, PASSWORD)
diseases = kg.get_diseases_by_symptoms(["Fever", "Joint Pain"])
print("Possible diseases:", diseases)

diseases = kg.get_diseases_by_symptoms(["Fever", "Joint Pain"])

for disease in diseases:
    treatments = kg.get_treatments_by_disease(disease)
    tests = kg.get_tests_by_disease(disease)
    print(f"\nDisease: {disease}")
    print(f"  Treatments: {treatments}")
    print(f"  Required Tests: {tests}")

kg.close()
