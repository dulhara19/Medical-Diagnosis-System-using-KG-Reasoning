import requests
import json

user_input = input("Enter something: ")
prompt = f"""
You are a professional medical assistant. Your job is to analyze user queries related to health symptoms and rewrite them clearly and medically for further processing.

- Focus on extracting relevant symptoms or medical complaints from the user's statement.
- Remove unnecessary words, emotions, or informal language.
- Keep the output short and medically clear — 1-2 sentences only.
- DO NOT diagnose or explain. Just clean up the sentence.
- Return only the simplified statement, no extra commentary or thinking.

Here are some examples:

---
User: "Hey, I've been feeling kinda dizzy and weird for the past few days."
→ Output: The patient reports dizziness.

User: "I've got a tight chest and I can't breathe properly!"
→ Output: The patient reports chest tightness and shortness of breath.

User: "I've had a bad headache and nausea since yesterday."
→ Output: The patient reports headache and nausea.

User: "My mom has been coughing non-stop and her fever won’t go down."
→ Output: The patient reports persistent cough and fever.

User: "I feel tired all the time and have trouble concentrating."
→ Output: The patient reports fatigue and difficulty concentrating.

---
Now simplify the following statement:
User: "{user_input}"
→ Output:" 
"""

url = 'http://localhost:11434/api/generate'
headers = {'Content-Type': 'application/json'}
data = {
    'model': 'deepseek-r1:8b',
    'prompt': prompt,
    'stream': False,  # not streaming
}

response = requests.post(url, headers=headers, data=json.dumps(data))

if response.status_code == 200:
    result = response.json()
    # clean unwanted tags like <think>
    answer = result.get("response", "").replace("<think>", "").replace("</think>", "").strip()
    print(answer)
else:
    print(f"Error: {response.status_code}")
    print(response.text)
