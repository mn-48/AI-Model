# import frappe
# import requests
# import json

# #  Explain quantum computing in simple terms

# @frappe.whitelist()
# # def call_ai_api(prompt):
# def add_numbers(prompt:str):

#     print("Received prompt:", prompt)
   

#     url = "http://127.0.0.1:11434/api/generate"


#     # gemma3:27b # *****
#     # deepseek-r1:8b #  ****
#     # llama3.2
#     # gpt-oss:20b
#     # gemma3

#     payload = {
#         "model": "gemma3",
#         "prompt": prompt,
#         "stream": True
#     }

#     r = ""

#     with requests.post(url, json=payload, stream=True) as r:
#         # return r

        
#         for line in r.iter_lines():
#             if line:
#                 data = json.loads(line)
#                 if "response" in data:
#                     print(data["response"], end="", flush=True)
#                     r += f"{data['response']}\n"
#     return r
    
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
