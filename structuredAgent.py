from llmconnector import connector
from sqlconnector import get_connection
from createresponse import create_response_from_llm
import re
from datetime import datetime

current_time = datetime.now().time()  # Gets current time (hours, minutes, seconds)
#print("Current time:", current_time)


def structuredAgent(user_input):

    prompt = f"""
You are a **medical center chatbot assistant** that converts natural language questions into MySQL queries.

Your job is to:
- Read the user input.
- Analyze whether it’s related to **appointments**, **doctor availability**, **lab test schedules**, or **pharmacy inventory**.
- Convert it into a valid **MySQL SELECT** query.
- Handle natural language date expressions like "today", "tomorrow", or weekdays.
- Wrap your SQL output **only** inside <final_answer> tags. Do not add any explanations or comments.
- Assume that the user will not add a question mark (?) at the end of their query, but treat every input as a question.

---

### Database Tables:

1. `appointments(patient_name, doctor_name, department, appointment_date, appointment_time)`
2. `doctor_availability(doctor_name, department, available_date, available_time, room_number)`
3. `lab_tests(test_name, test_type, available_date, available_time)`
4. `pharmacy_items(item_name, item_type, quantity_in_stock, price)`

---

### Mapping Rules:

- "today" → `CURRENT_DATE()`
- "tomorrow" → `CURRENT_DATE() + INTERVAL 1 DAY`
- Weekdays like "Monday", "Tuesday" → `day_of_week = 'Monday'` etc.
- "available doctors", "doctor availability", "who is available" → `doctor_availability`
- "appointments", "my appointment", "checkup" → `appointments`
- "test", "blood test", "urine test", etc. → `lab_tests`
- "pharmacy", "medicine", "drugs", "buy", "painkiller" → `pharmacy_items`

---

### Output Format:
```<final_answer>[SQL_QUERY]</final_answer>```

---

### Examples:

User: "What appointments are scheduled for today?"
→ <final_answer>SELECT patient_name, doctor_name, department, appointment_time FROM appointments WHERE appointment_date = CURRENT_DATE();</final_answer>

User: "Is Dr. Silva available tomorrow?"
→ <final_answer>SELECT doctor_name, department, available_time, room_number FROM doctor_availability WHERE doctor_name LIKE '%Silva%' AND available_date = CURRENT_DATE() + INTERVAL 1 DAY;</final_answer>

User: "What lab tests are available on Monday?"
→ <final_answer>SELECT test_name, test_type, available_time FROM lab_tests WHERE DAYNAME(available_date) = 'Monday';</final_answer>

User: "What medicine is available for fever?"
→ <final_answer>SELECT item_name, item_type, quantity_in_stock, price FROM pharmacy_items WHERE item_name LIKE '%fever%';</final_answer>

---

Now generate the SQL query for the following user input:

 "{user_input}"
   """

    print("agent called for structured question")
    response=connector(prompt)  # Call the connector function with user input
    
# Parse and extract classification
    result = response.json()
    raw_output = result.get("response", "")

# Print raw output for debugging
    print("\n📦 Raw LLM Output:\n", raw_output)

# Step 5: Extract <final_answer>
    match = re.search(r"<final_answer>\s*(.*?)\s*</final_answer>", raw_output, re.DOTALL | re.IGNORECASE)

    if match:
       query = match.group(1).strip()
       print("\n✅ qery generated:")
       print(query)
       conn=get_connection()
       cursor=conn.cursor()
       cursor.execute(query)
       all_rows = cursor.fetchall()

       print("\n✅ Query Results generated:")

       response=create_response_from_llm(all_rows, user_input,query,current_time)

       # Step 4: Parse and extract classification
       result = response.json()
       raw_output = result.get("response", "")

      # Print raw output for debugging
      # print("\n📦 Raw LLM Output:\n", raw_output)

      # Step 5: Extract <final_answer>
       match = re.search(r"<final_answer>\s*(.*?)\s*</final_answer>", raw_output, re.DOTALL | re.IGNORECASE)
       if match:
          final_answer = match.group(1).strip()
          print("\n✅ Final Answer Extracted:")
        # print(final_answer)
    return final_answer         

# structuredAgent("When is the bus to kadawatha arriving at the main gate?")