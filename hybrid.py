import requests
import json
import re

# from neragent import extract_symptoms_ner

def calling_hybridAgent(user_input):
  prompt = f"""
You are a helpful assistant specialized in understanding user inputs in medical contexts. A user may input a hybrid sentence that includes both:

1. A **symptom story** (describing patient symptoms over time), and  
2. A **direct medical question** (asking for a definition or explanation, like "What is dry cough?").

🎯 Your task is to extract and classify the input into these two parts using the following format:

{
  "symptom_story": "<Extracted story content describing the symptoms>",
  "question": "<Extracted direct question if any, or leave empty if not present>"
}

🧠 Make sure:
- The symptom story includes anything related to physical/mental symptoms, their timing, and changes.
- The question part includes only the actual question being asked.

📥 Example input:
"Patient has a headache and fever, but no other symptoms. But he was having muscle pain yesterday. Dizzy and vomiting as well. He was also having a runny nose and sore throat last week. He has been feeling fatigued for the past few days, but no other symptoms are present. Also my head was hurting a lot. What is dry cough?"

📤 Expected output:
{
  "symptom_story": "Patient has a headache and fever, but no other symptoms. But he was having muscle pain yesterday. Dizzy and vomiting as well. He was also having a runny nose and sore throat last week. He has been feeling fatigued for the past few days, but no other symptoms are present. Also my head was hurting a lot.",
  "question": "What is dry cough?"
}

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