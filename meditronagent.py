import requests
import json
import re
import subprocess
# from neragent import extract_symptoms_ner

user_input = input("Enter something: ")
prompt = f"""
You are a professional medical assistant. Your job is to analyze user queries related to health symptoms and rewrite them clearly and medically for further processing.

- Focus on extracting relevant symptoms or medical complaints from the user's statement.
- Keep the output short and medically clear.
- DO NOT diagnose or explain. Just clean up the sentence but dont cut or remove any symptoms.
- Return only the simplified statement, no extra commentary or thinking.
- avoid judging the desease according to the user query, just rewrite it in a medical way.

Here are some examples:

---
User: "Hey, I've been feeling kinda dizzy and weird for the past few days.also my head was hurting a lot."
→ Output: The patient reports dizziness and headache.

User: "I've got a tight chest and I can't breathe properly!"
→ Output: The patient reports chest tightness and shortness of breath.

User: "I've had a bad headache and nausea since yesterday."
→ Output: The patient reports headache and nausea.

User: "My mom has been coughing non-stop and her fever won’t go down."
→ Output: The patient reports persistent cough and fever.

User: "I feel tired all the time and have trouble concentrating."
→ Output: The patient reports fatigue and difficulty concentrating.

- when User gives a long statement according to the given instructions put the Output in <final_answer> tags and do not   print anything else.

give the final answer after thinking must be in the format as follows: 
<final_answer>
→ Output
</final_answer>
---
Now simplify the following statement:
User: "{user_input}"
→ Output:" 

if user asks diseases related questions along with the query like, 

User: "What are the symptoms of the common cold?"

User: "What causes the seasonal flu?"

User:"What medication would be prescribed for a headache?"

add <disease></>

"""



url = 'http://localhost:11434/api/generate'
headers = {'Content-Type': 'application/json'}
data = {
    'model': 'meditron:7b-q6_K ',
    'prompt': prompt,
    'stream': False,  # not streaming
}

response = requests.post(url, headers=headers, data=json.dumps(data))