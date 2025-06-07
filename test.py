# from neragent import extract_symptoms_ner

# nswer=extract_symptoms_ner("Patient has a headache and fever, but no other symptoms.but he was having muscle pain yesteray. dizzy and vomiting as well. He was also having a runny nose and sore throat last week. He has been feeling fatigued for the past few days, but no other symptoms are present.also my head was hurting a lot")


import requests
import json
import re

# from neragent import extract_symptoms_ner

def calling_hybridAgent(user_input):
  prompt = f"""
You are a medical language understanding agent.

Your job is to carefully read a user's input and extract structured information in the following categories:

1. symptoms: all health issues mentioned (e.g., headache, fever, fatigue)
2. time_periods: durations or references to time (e.g., "since yesterday", "for the past week")
3. direct_questions: any explicit questions the user is asking (e.g., "What is dry cough?")
4. subject: who is experiencing the symptoms (e.g., "my son", "I", "the patient")

Format your output as a JSON object:

{
  "subject": "...",
  "symptoms": [...],
  "time_periods": [...],
  "direct_questions": [...]
}

---

📥 Example 1:
"I’ve been feeling dizzy and had a sore throat for two days. What is pharyngitis?"

📤 Output:
{
  "subject": "I",
  "symptoms": ["dizzy", "sore throat"],
  "time_periods": ["for two days"],
  "direct_questions": ["What is pharyngitis?"]
}

---

📥 Example 2:
"My brother has had chills, fever, and a dry cough since last Friday. Is it COVID?"

📤 Output:
{
  "subject": "my brother",
  "symptoms": ["chills", "fever", "dry cough"],
  "time_periods": ["since last Friday"],
  "direct_questions": ["Is it COVID?"]
}

---

📥 Example 3:
"I was vomiting yesterday and had muscle cramps. I’m also really weak today."

📤 Output:
{
  "subject": "I",
  "symptoms": ["vomiting", "muscle cramps", "weak"],
  "time_periods": ["yesterday", "today"],
  "direct_questions": []
}

---

📥 Example 4:
"The patient had joint pain last week and is now experiencing fatigue. What test is recommended?"

📤 Output:
{
  "subject": "the patient",
  "symptoms": ["joint pain", "fatigue"],
  "time_periods": ["last week", "now"],
  "direct_questions": ["What test is recommended?"]
}

---

Now analyze the following input and extract the structured information using the same format:

"""


  url = 'http://localhost:11434/api/generate'
  headers = {'Content-Type': 'application/json'}
  data = {
    'model': 'deepseek-r1:8b',
    'prompt': prompt,
    'stream': False,  # not streaming
  }

  response = requests.post(url, headers=headers, data=json.dumps(data))


# Get and print final answer from <final_answer> tags
  result = response.json()
  raw_output = result.get("response", "")

  match = re.search(r"<final_answer>\s*(.*?)\s*</final_answer>", raw_output, re.DOTALL | re.IGNORECASE)
  if match:
      final_answer = match.group(1).strip()
      print("\n✅ Final Answer Extracted:")
      print(final_answer)
      return final_answer
  else:
      print("\n❌ No <final_answer> tag found in the response.")
