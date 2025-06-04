import requests
import json
import re
import subprocess
# from neragent import extract_symptoms_ner


def calling_meditron(user_input):
    # print(f"🔍 Processing input: '{user_input}'")
    # Here you would call your Meditron model or any other LLM to get the answer
    # For now, we just simulate a response
    
  
    prompt = user_input


    url = 'http://localhost:11434/api/generate'
    headers = {'Content-Type': 'application/json'}
    data = {
    'model': 'meditron:7b-q6_K',
    'prompt': prompt,
    'stream': False,  # not streaming
    }

    response = requests.post(url, headers=headers, data=json.dumps(data))
    return response 

# answer = calling_meditron("what is dry cough")
# print(answer.json())