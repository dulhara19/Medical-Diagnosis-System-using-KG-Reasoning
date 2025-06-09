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

Format your output as a JSON object.

⚠️ Important: Wrap the final output JSON inside <final_answer>...</final_answer> tags.

Example format:

<final_answer>
{{
  "subject": "...",
  "symptoms": [...],
  "time_periods": [...],
  "direct_questions": [...]
}}
</final_answer>

---

📥 Example 1:
"I’ve been feeling dizzy and had a sore throat for two days. What is pharyngitis?"

📤 Output:
<final_answer>
{{
  "subject": "I",
  "symptoms": ["dizzy", "sore throat"],
  "time_periods": ["for two days"],
  "direct_questions": ["What is pharyngitis?"]
}}
</final_answer>

---

📥 Example 2:
"My brother has had chills, fever, and a dry cough since last Friday. Is it COVID?"

📤 Output:
<final_answer>
{{
  "subject": "my brother",
  "symptoms": ["chills", "fever", "dry cough"],
  "time_periods": ["since last Friday"],
  "direct_questions": ["Is it COVID?"]
}}
</final_answer>

---

📥 Example 3:
"I was vomiting yesterday and had muscle cramps. I’m also really weak today."

📤 Output:
<final_answer>
{{
  "subject": "I",
  "symptoms": ["vomiting", "muscle cramps", "weak"],
  "time_periods": ["yesterday", "today"],
  "direct_questions": []
}}
</final_answer>

---

📥 Example 4:
"The patient had joint pain last week and is now experiencing fatigue. What test is recommended?"

📤 Output:
<final_answer>
{{
  "subject": "the patient",
  "symptoms": ["joint pain", "fatigue"],
  "time_periods": ["last week", "now"],
  "direct_questions": ["What test is recommended?"]
}}
</final_answer>

---

📥 Example 5:
"My son has been coughing badly for three days, and now he’s also got a fever. Should I be worried?"

📤 Output:
<final_answer>
{{
  "subject": "my son",
  "symptoms": ["coughing", "fever"],
  "time_periods": ["for three days", "now"],
  "direct_questions": ["Should I be worried?"]
}}
</final_answer>

---

📥 Example 6:
"I was sneezing a lot this morning and now my nose won’t stop running. What could this mean?"

📤 Output:
<final_answer>
{{
  "subject": "I",
  "symptoms": ["sneezing", "runny nose"],
  "time_periods": ["this morning", "now"],
  "direct_questions": ["What could this mean?"]
}}
</final_answer>

---

📥 Example 7:
"My grandma has been complaining of back pain and dizziness for the past few days."

📤 Output:
<final_answer>
{{
  "subject": "my grandma",
  "symptoms": ["back pain", "dizziness"],
  "time_periods": ["for the past few days"],
  "direct_questions": []
}}
</final_answer>

---

📥 Example 8:
"Feeling exhausted all the time. I also get lightheaded if I stand too quickly. What’s going on?"

📤 Output:
<final_answer>
{{
  "subject": "I",
  "symptoms": ["exhausted", "lightheaded"],
  "time_periods": ["all the time", "if I stand too quickly"],
  "direct_questions": ["What’s going on?"]
}}
</final_answer>

---

Now analyze the following input and extract the structured information using the same format:

{user_input}
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


calling_hybridAgent("Patient has a headache and fever, but no other symptoms.but he was having muscle pain yesteray. dizzy and vomiting as well. He was also having a runny nose and sore throat last week. He has been feeling fatigued for the past few days, but no other symptoms are present.also my head was hurting a lot")