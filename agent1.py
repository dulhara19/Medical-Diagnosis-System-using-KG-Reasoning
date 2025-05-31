import requests
import json

user_input = input("Enter something: ")
promt = "according this user input: " + user_input + ", what are the symptomps? Please answer in comma seperated words, no explanation needed and dont give chain of thoughts as well. If you don't know, just say 'unknown'."

url = 'http://localhost:11434/api/generate'
headers = {'Content-Type': 'application/json'}
data = {
    'model': 'deepseek-r1:1.5b',
    'prompt': promt,
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
