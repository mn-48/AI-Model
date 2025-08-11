
import requests
import json

url = "http://127.0.0.1:11434/api/generate"


# gemma3:27b # *****
# deepseek-r1:8b #  ****
# llama3.2
# gpt-oss:20b
# gemma3

payload = {
    "model": "deepseek-r1:8b",
    "prompt": "Explain quantum computing in simple terms",
    "stream": True
}

with requests.post(url, json=payload, stream=True) as r:
    for line in r.iter_lines():
        if line:
            data = json.loads(line)
            if "response" in data:
                print(data["response"], end="", flush=True)
