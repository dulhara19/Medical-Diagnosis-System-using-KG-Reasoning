# Multi Agentic Medical Diagnosis System using KG Reasoning(under development)

This project is a multi agentic medical diagnosis system that leverages a Knowledge Graph (KG) stored in Neo4j to reason about possible diseases based on user-provided symptoms. It can also suggest treatments and required tests for the diagnosed diseases. also when agents can identify the wether user is requesting details about diseases or telling a story including all the deatils of current sysmptoms or story with specific question about disease. it can call another agents to work together to answer the user.  

## Features

- Connects to a Neo4j database using credentials from a `.env` file.
.- handle multiple agents
- Finds possible diseases based on a list of symptoms, with a confidence score.
- Retrieves treatments and required tests for a given disease.
- idenify user query and call relevant agents accordingly
- currently there are 3 agents working together
- connect meditron if user askes questions about diseases (ex: what is dry cough?)
- connects knowledge graph if user says symptoms and relevant disease
- if user say a story mentioning both type of questions, query redirects to another agent which capabale of handling both  


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

