import requests
import json
import re

# from neragent import extract_symptoms_ner

def calling_hybridAgent(user_input):
  prompt = f"""
You are a smart medical language analyzer.

Users may input a hybrid sentence that includes:
1. A <story>: symptom description about the patient, their health history, or how they feel.
2. A <direct>: specific question asking for information (e.g., “What is dry cough?”).

🧠 Your task:
- Identify and classify each part clearly inside these tags:
  - <story> ... </story>
  - <direct> ... </direct>
- If the input only contains a story, leave <direct> empty.
- If it only contains a direct question, leave <story> empty.

Format your response like this:
<story>...</story>
<direct>...</direct>

---

📥 Example 1:
"Patient has headache and dizziness. Also had vomiting last night. What is meningitis?"

📤 Output:
<story>Patient has headache and dizziness. Also had vomiting last night.</story>  
<direct>What is meningitis?</direct>

---

📥 Example 2:
"My son has had fever and chills for three days. He also developed body pain and a rash today. Is it dengue or something else?"

📤 Output:
<story>My son has had fever and chills for three days. He also developed body pain and a rash today.</story>  
<direct>Is it dengue or something else?</direct>

---

📥 Example 3:
"What are the symptoms of tuberculosis?"

📤 Output:
<story></story>  
<direct>What are the symptoms of tuberculosis?</direct>

---

📥 Example 4:
"I feel really weak lately, and I keep having joint pain. My appetite is very low and I get tired quickly."

📤 Output:
<story>I feel really weak lately, and I keep having joint pain. My appetite is very low and I get tired quickly.</story>  
<direct></direct>

---

📥 Example 5:
"Patient has a headache and fever, but no other symptoms. He was having muscle pain yesterday. Dizzy and vomiting as well. He was also having a runny nose and sore throat last week. Feeling fatigued for the past few days. What is dry cough?"

📤 Output:
<story>Patient has a headache and fever, but no other symptoms. He was having muscle pain yesterday. Dizzy and vomiting as well. He was also having a runny nose and sore throat last week. Feeling fatigued for the past few days.</story>  
<direct>What is dry cough?</direct>

---

Now analyze the following input and classify it using the same format:

"""


  url = 'http://localhost:11435/api/generate'
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


#----start----from here i try to send data throuhgh subprocess to the other env and run the script because currently i had issue with the import of neragent.py in this env, so i am trying to run it through subprocess and send the final_answer to it. just because i needed to use scispacy library in my current python version but it didnt support it, so i created another env with python 3.10 and installed the required packages there. now i am trying to run the neragent.py script in that env using subprocess and send the final_answer to it. lets keep this as a temporary solution until i find a better way to handle this.-------------

# # Activate the other env and run the script
# process = subprocess.run(
#     ['C:/AI-projects/Medical Diagnosis - KG Reasoning/venv310/Scripts/python.exe',
#      'C:/AI-projects/Medical Diagnosis - KG Reasoning/neragent.py',
#      final_answer],
#     capture_output=True,
#     text=True
# )
#----------end---------------