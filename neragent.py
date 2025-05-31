import spacy

# Load the SciSpacy NER model
nlp = spacy.load("en_ner_bc5cdr_md")

def extract_symptoms_ner(text):
    """
    Extracts disease/symptom entities using SciSpacy's biomedical NER model.
    :param text: str, user input
    :return: list of recognized symptoms/diseases
    """
    doc = nlp(text)
    symptoms = [ent.text for ent in doc.ents if ent.label_ == "DISEASE"]
    return symptoms
 
answer=extract_symptoms_ner("Patient has a headache and fever, but no other symptoms.")
print(answer)