import requests
import json
import re
import subprocess
# from neragent import extract_symptoms_ner

def calling_llmagent(user_input):
  prompt = f"""
You are a professional medical assistant. Your job is to analyze user queries related to health symptoms and rewrite them clearly and medically for further processing.

Instructions:
- Extract all relevant symptoms or medical complaints from the user's statement.
- Rewrite it in a medically clear and short format.
- DO NOT explain, diagnose, or skip any symptoms.
- Avoid extra commentary.
- Your output MUST be wrapped in <final_answer> and </final_answer> tags.

Examples:

User: "Hey, I've been feeling kinda dizzy and weird for the past few days. also my head was hurting a lot."
<final_answer>
→ The patient reports dizziness and headache.
</final_answer>

User: "I've got a tight chest and I can't breathe properly!"
<final_answer>
→ The patient reports chest tightness and shortness of breath.
</final_answer>

User: "I've had a bad headache and nausea since yesterday."
<final_answer>
→ The patient reports headache and nausea.
</final_answer>

User: "My mom has been coughing non-stop and her fever won’t go down."
<final_answer>
→ The patient reports persistent cough and fever.
</final_answer>

User: "I feel tired all the time and have trouble concentrating."
<final_answer>
→ The patient reports fatigue and difficulty concentrating.
</final_answer>

User: "Last night I started vomiting, then had chills and my whole body started to ache. I couldn't sleep at all."
<final_answer>
→ The patient reports vomiting, chills, body aches, and insomnia.
</final_answer>

User: "For the past week, I've had a sore throat and stuffy nose. Now I've developed a slight fever and a dry cough too."
<final_answer>
→ The patient reports sore throat, nasal congestion, fever, and dry cough.
</final_answer>

User: "I've been waking up in the middle of the night sweating. Also feel nauseous in the mornings and sometimes dizzy."
<final_answer>
→ The patient reports night sweats, morning nausea, and dizziness.
</final_answer>

User: "I'm coughing up green mucus, my head hurts, and I feel super weak and tired all day."
<final_answer>
→ The patient reports productive cough with green mucus, headache, weakness, and fatigue.
</final_answer>

User: "It's hard to explain, but my legs feel tingly and I get random muscle twitches. Also some lower back pain."
<final_answer>
→ The patient reports leg tingling, muscle twitches, and lower back pain.
</final_answer>

Now simplify the following statement:
User: "{user_input}"
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