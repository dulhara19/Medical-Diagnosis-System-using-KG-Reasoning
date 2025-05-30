# Medical Diagnosis System using KG Reasoning

This project is a medical diagnosis system that leverages a Knowledge Graph (KG) stored in Neo4j to reason about possible diseases based on user-provided symptoms. It can also suggest treatments and required tests for the diagnosed diseases.

## Features

- Connects to a Neo4j database using credentials from a `.env` file.
- Finds possible diseases based on a list of symptoms, with a confidence score.
- Retrieves treatments and required tests for a given disease.

## Requirements

- Python 3.7+
- Neo4j database (running locally or remotely)
- Python packages:
  - `neo4j`
  - `python-dotenv`

## Setup

1. **Clone the repository** and navigate to the project directory.

2. **Install dependencies**:
   ```sh
   pip install neo4j python-dotenv

3. **Configure environment variables**
Create a .env file in the project root (already present in this repo) with the following content:
 
  ```sh
    NEO4J_URI=bolt://localhost:7687
    NEO4J_USER=your_username
    NEO4J_PASSWORD=your_password
  ```

4. Ensure your Neo4j database is running and contains nodes and relationships for Symptom, Disease, Drug, and Test.

**Code Structure**

app.py: Main application file containing the MedicalKG class and usage example.

.env: Environment variables for Neo4j connection.

Customization:
Update the Cypher queries in app.py to match your Neo4j data model if needed.

Extend the MedicalKG class with more methods for additional reasoning capabilities.

This project is for educational purposes. feel free to pull request. also im seeking collaborations for the project 
made by Dulhara :)

