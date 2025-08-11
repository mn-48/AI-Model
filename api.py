import frappe
import requests
import json

@frappe.whitelist()
def add_numbers(prompt: str):
    print("Received prompt:", prompt)

    url = "http://127.0.0.1:11434/api/generate"

    payload = {
        "model": "gemma3",
        "prompt": prompt,
        "stream": True
    }

    result_text = ""  # এখানে string জমাবো

    with requests.post(url, json=payload, stream=True) as resp:
        for line in resp.iter_lines():
            if line:
                data = json.loads(line)
                if "response" in data:
                    print(data["response"], end="", flush=True)
                    result_text += f"{data['response']}\n"
    return result_text


# -----------------------------------------------------------------------------


import frappe
import requests
import json
import re

AI_URL = "http://127.0.0.1:11434/api/generate"
MODEL_NAME = "gemma3"  # তোমার AI মডেল

def get_db_schema():
    """পুরো MariaDB স্কিমা রিটার্ন করবে"""
    schema = {}
    tables = frappe.db.sql("SHOW TABLES", as_dict=False)
    for t in tables:
        table_name = t[0]
        columns = frappe.db.sql(f"DESCRIBE `{table_name}`", as_dict=True)
        schema[table_name] = columns
    return schema

def is_safe_sql(query):
    """SQL সেফ কিনা চেক করবে"""
    query_lower = query.strip().lower()
    # শুধু SELECT, SHOW, DESCRIBE, EXPLAIN অনুমতি দেবে
    return query_lower.startswith(("select", "show", "describe", "explain"))

@frappe.whitelist()
def ai_database_agent(prompt: str):
    print("Received prompt:", prompt)

    # ডাটাবেস স্কিমা বের করা
    schema = get_db_schema()

    # AI Prompt তৈরি
    final_prompt = f"""
    You are a SQL expert. Based on the following database schema, write an SQL query to answer the user request.
    Schema:
    {json.dumps(schema, indent=2)}

    User request:
    {prompt}

    Return only the SQL query without explanation.
    """

    # AI কল
    payload = {
        "model": MODEL_NAME,
        "prompt": final_prompt,
        "stream": False
    }

    resp = requests.post(AI_URL, json=payload)
    ai_response = resp.json().get("response", "").strip()

    # AI Response থেকে SQL এক্সট্র্যাক্ট
    sql_query = re.sub(r"```sql|```", "", ai_response).strip()

    print("AI Generated SQL:", sql_query)

    # সেফটি চেক
    if not is_safe_sql(sql_query):
        return {"error": "Unsafe SQL query detected. Only read operations allowed."}

    # SQL রান করে রেজাল্ট আনা
    try:
        db_result = frappe.db.sql(sql_query, as_dict=True)
    except Exception as e:
        return {"error": str(e), "sql": sql_query}

    return {
        "sql": sql_query,
        "result": db_result
    }
