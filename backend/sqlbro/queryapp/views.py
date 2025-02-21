import os
import json
import google.generativeai as genai
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.db import connection
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Set up Gemini API Key
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# Function to generate MySQL query from natural language
def generate_sql_from_natural_language(user_input):
    prompt = f"""
    Convert the following natural language instruction into a MySQL query:
    
    Instruction: "{user_input}"
    
    Rules:
    - If creating a table, use proper data types like INT, VARCHAR, TIMESTAMP, etc.
    - If inserting data, ensure it matches the table structure.
    - If selecting data, ensure proper SQL syntax.
    - Return only the SQL query, no explanations.
    
    SQL Query:
    """

    model = genai.GenerativeModel("gemini-pro")
    response = model.generate_content(prompt)
    
    return response.text.strip() if response.text else None

@csrf_exempt
def execute_natural_query(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            user_input = data.get("query", "")

            # Convert natural language to SQL
            sql_query = generate_sql_from_natural_language(user_input)

            if not sql_query:
                return JsonResponse({"status": "error", "message": "Failed to generate SQL query"})

            with connection.cursor() as cursor:
                cursor.execute(sql_query)

                # Fetch column names
                columns = [col[0] for col in cursor.description] if cursor.description else []

                # Handle SELECT and DESCRIBE queries
                if sql_query.strip().lower().startswith(("select", "describe", "show")):
                    results = cursor.fetchall()
                    return JsonResponse({
                        "status": "success",
                        "columns": columns,
                        "results": results
                    })

                return JsonResponse({"status": "success", "message": "Query executed successfully"})

        except Exception as e:
            return JsonResponse({"status": "error", "message": str(e)})

    return JsonResponse({"status": "error", "message": "Invalid request"}, status=400)

