import openai

def extract_symptoms_llm(prompt):
    openai.api_key = "YOUR_API_KEY"
    
    system_prompt = "You are a medical assistant. Extract only the medical symptoms from the user's text as a list."
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": prompt}
        ]
    )
    return response.choices[0].message.content.strip()
