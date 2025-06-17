# neragent.py
import spacy
import sys

# Load the SciSpacy biomedical NER model
nlp = spacy.load("en_ner_bc5cdr_md")

def calling_neragent(text):
    """
    Extracts disease/symptom entities using SciSpacy's biomedical NER model.
    """
    doc = nlp(text)
    symptoms = [ent.text for ent in doc.ents if ent.label_ == "DISEASE"]
    return symptoms




# answer=calling_neragent("The patient reports fatigue and difficulty concentrating")
# print(answer)