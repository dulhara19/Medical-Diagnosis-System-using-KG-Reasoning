import requests
import json
import re
from meditron import calling_meditron 
# Step 1: User input
user_input = input(" Enter your medical question or story: ")

# Step 2: Formulate the prompt with richer examples
prompt = f"""
You are a classifier that determines whether a user input is a medical "information question", "symptom story", or a "hybrid".

Your task is to output ONLY one of these three categories wrapped inside <final_answer> tags:
- info_question → asking for factual medical information
- symptom_story → describing symptoms or a health condition
- hybrid → contains both a question and symptoms

Examples:
- "What is dry cough?" → <final_answer>info_question</final_answer>
- "What are the symptoms of the common cold?" → <final_answer>info_question</final_answer>
- "What causes the seasonal flu?" → <final_answer>info_question</final_answer>
- "What medication would be prescribed for a headache?" → <final_answer>info_question</final_answer>
- "How can I treat a sore throat?" → <final_answer>info_question</final_answer> 
- "Can you explain shortness of breath?" → <final_answer>info_question</final_answer>

- "I've had nausea and fever since last night." → <final_answer>symptom_story</final_answer>
- "I have a headache and feel dizzy." → <final_answer>symptom_story</final_answer>
- "My chest feels tight and I can't breathe well." → <final_answer>symptom_story</final_answer>
- "I have a runny nose and sore throat." → <final_answer>symptom_story</final_answer>

- "Patient has a headache and fever, but no other symptoms. But he was having muscle pain yesterday. Dizzy and vomiting as well. He was also having a runny nose and sore throat last week. He has been feeling fatigued for the past few days, but no other symptoms are present. Also my head was hurting a lot. What is dry cough?" → <final_answer>hybrid</final_answer>
- "I have a headache and feel dizzy. What is dry cough?" → <final_answer>hybrid</final_answer>
- "My chest feels tight and I can't breathe well. What are the symptoms of the common cold?" → <final_answer>hybrid</final_answer>
- "I have a runny nose and sore throat. What causes the seasonal flu?" → <final_answer>hybrid</final_answer>
- "Can you explain shortness of breath? What medication would be prescribed for a headache?" → <final_answer>hybrid</final_answer>
- "What is dry cough? I've had nausea and fever since last night." → <final_answer>hybrid</final_answer>
- "What are the symptoms of the common cold? I have a headache and feel dizzy." → <final_answer>hybrid</final_answer>

Now classify this input:
"{user_input}"
→
"""

# Step 3: Send request to LLM
url = 'http://localhost:11435/api/generate'
headers = {'Content-Type': 'application/json'}
data = {
    'model': 'deepseek-r1:8b',
    'prompt': prompt,
    'stream': False,  # Not using streaming
}

response = requests.post(url, headers=headers, data=json.dumps(data))

# Step 4: Parse and extract classification
result = response.json()
raw_output = result.get("response", "")

# Print raw output for debugging
print("\n📦 Raw LLM Output:\n", raw_output)

# Step 5: Extract <final_answer>
match = re.search(r"<final_answer>\s*(.*?)\s*</final_answer>", raw_output, re.DOTALL | re.IGNORECASE)




# --------- AGENT FUNCTIONS ---------
def info_question_agent(user_input):
    print("\n🤖 [INFO AGENT]: Answering factual medical question...")
    
    answer = calling_meditron(user_input)
    print(f"🔍 Processing info question: '{user_input}'")
        # Here you would call your Meditron model or any other LLM to get the answer
        # For now, we just simulate a response
    print(f"🧠 Answering info: '{answer}'")


        


def symptom_story_agent(user_input):
    print("\n🧬 [SYMPTOM AGENT]: Understanding symptoms and reasoning...")
    # Your logic to do symptom extraction, NER, call KG, etc.
    print(f"🩺 Diagnosing from: '{user_input}'")


def hybrid_agent(user_input):
    print("\n🔀 [HYBRID AGENT]: Handling both symptom story and question...")
    # You can call both agents or do smarter hybrid logic
    info_question_agent(user_input)
    symptom_story_agent(user_input)





if match:
    final_answer = match.group(1).strip()
    print("\n✅ Final Answer Extracted:")
    print(final_answer)

# --------- ROUTING TO AGENTS ---------
    if final_answer == "info_question":
        info_question_agent(user_input)
    elif final_answer == "symptom_story":
        symptom_story_agent(user_input)
    elif final_answer == "hybrid":
        hybrid_agent(user_input)
    else:
        print("⚠️ Unknown classification.")
else:
    print("\n❌ No <final_answer> tag found in the response.")


