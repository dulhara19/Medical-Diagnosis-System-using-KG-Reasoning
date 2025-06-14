import requests
import json


def connector(prompt):
    url = 'http://localhost:11434/api/generate'
    headers = {'Content-Type': 'application/json'}
    data = {
       'model': 'deepseek-r1:8b',
       'prompt': prompt,
       'stream': False,  # Not using streaming
           }

    response = requests.post(url, headers=headers, data=json.dumps(data))
    return response