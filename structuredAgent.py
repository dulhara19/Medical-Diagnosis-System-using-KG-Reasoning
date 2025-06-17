from llmconnector import connector
from sqlconnector import get_connection
from createresponse import create_response_from_llm
import re
from datetime import datetime

current_time = datetime.now().time()  # Gets current time (hours, minutes, seconds)
#print("Current time:", current_time)


def structuredAgent(user_input):

    prompt = f"""
    You are a university chatbot assistant that converts natural language questions into MySQL queries.

    Your job is to:
    - Read the user input.
    - Analyze whether it's related to timetables, bus schedules, or café menus.
    - Convert it into a valid MySQL SELECT query.
    - Handle natural language date expressions like "today", "tomorrow", or weekdays.
    - Wrap your SQL output **only** inside <final_answer> tags. Do not add any explanations or comments.
    - user will not put ? at the end of the question. but consider every query as a question. 

Database tables:

1. `timetables(course_name, lecturer_name, location, start_time, end_time, date, day_of_week)`
2. `bus_schedules(route_name, departure_location, arrival_location, departure_time, arrival_time, date, day_of_week)`
3. `cafe_menus(item_name, item_type, price, date, day_of_week)`

Instructions:
- departure_location is 'University Main Gate' if user says "main gate" or "campus" or even if user didnt mention it.
- departure_location is 'Sports Complex' if user says "campus sport center" or "rec" or "recreational center".
- arrival_locations are (Panadura,Kaduwela,Gampaha,Kadawatha,Moratuwa,Horana,Kaluthara,Athurugiriya,Pettah,Nugegoda)
- 


Mapping Rules:
- "today" → `CURRENT_DATE()`
- "tomorrow" → `CURRENT_DATE() + INTERVAL 1 DAY`
-  Weekdays like "Monday", "Tuesday" → `day_of_week = 'Monday'` etc.
-  "main gate" → `departure_location = 'University Main Gate'`
-  "campus" → `departure_location = 'University Main Gate'`
- 

Output format:
```<final_answer>[SQL_QUERY]</final_answer>```

Examples:

User: "What’s on the cafe menu today?"  
→ <final_answer>SELECT item_name, item_type, price FROM cafe_menus WHERE date = CURRENT_DATE();</final_answer>






User: "when is the bus to kadawatha arriving at the main gate?"
→ <final_answer>SELECT route_name, departure_time, arrival_time FROM bus_schedules WHERE departure_location ='University Main Gate' AND date = CURRENT_DATE() AND arrival_location='Kadawatha' ;
</final_answer>

User: "What are the bus schedules for today"
→ <final_answer>SELECT route_name, departure_time, arrival_time FROM bus_schedules WHERE departure_location ='University Main Gate' AND date = CURRENT_DATE();</final_answer>

User: "When does the bus leave from campus to Athurugiriya tomorrow?"  
→ <final_answer>SELECT route_name, departure_time, arrival_time FROM bus_schedules WHERE departure_location ='University Main Gate' AND arrival_location LIKE '%Athurugiriya%' AND date = CURRENT_DATE() + INTERVAL 1 DAY;</final_answer>





User: "What time is the software engineering lecture on Wednesday?"  
→ <final_answer>SELECT course_name, start_time, end_time, location FROM timetables WHERE course_name LIKE '%software engineering%' AND day_of_week = 'Wednesday';</final_answer>

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