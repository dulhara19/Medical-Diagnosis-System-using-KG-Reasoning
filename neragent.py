# neragent.py
import spacy
import sys

# Load the SciSpacy biomedical NER model
nlp = spacy.load("en_ner_bc5cdr_md")

def extract_symptoms_ner(text):
    """
    Extracts disease/symptom entities using SciSpacy's biomedical NER model.
    """
    doc = nlp(text)
    symptoms = [ent.text for ent in doc.ents if ent.label_ == "DISEASE"]
    return symptoms

if __name__ == "__main__":
    symptom_text = sys.argv[1]
    symptoms = extract_symptoms_ner(symptom_text)
    print("::, ".join(symptoms))  # Output as plain string for capture

# diagnosis_pipeline.py






# answer=extract_symptoms_ner("Patient has a headache and fever, but no other symptoms.but he was having muscle pain yesteray. dizzy and vomiting as well. He was also having a runny nose and sore throat last week. He has been feeling fatigued for the past few days, but no other symptoms are present.also my head was hurting a lot.")
# print(answer)