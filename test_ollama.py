import requests

# Define the local API endpoint
OLLAMA_URL = "http://localhost:11434/api/generate"

# Define the request payload
payload = {
    "model": "llama3.2:3b-instruct-q4_K_M",
    "prompt": "Explain the benefits of running AI models locally.",
    "system": "You are an assistant who explains concepts clearly and concisely.",
    "stream": False
}

# Make the POST request
response = requests.post(OLLAMA_URL, json=payload)

# Check response
if response.status_code == 200:
    print("Response:", response.json()["response"])
else:
    print("Error:", response.status_code, response.text)