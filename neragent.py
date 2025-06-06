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


# if __name__ == "__main__":
#     symptom_text = sys.argv[1]
#     symptoms = extract_symptoms_ner(symptom_text)
#     print("::, ".join(symptoms))  # Output as plain string for capture

# diagnosis_pipeline.py






# answer=calling_neragent("The patient reports fatigue and difficulty concentrating")
# print(answer)