import requests
import json

print("Hello! Let's create a new parameter together 😊")
print("I need some info from you to do that (press Enter after you have inserted the answer)")

# Prompt for input
domain = input("🌍 Enter the domain (e.g., https://api.example.com): ").strip()
param_name = input("🩺 Enter the parameter name: ").strip()
data_type = input("🔢 Enter the data type (e.g., NUMERIC, STRING): ").strip()

# Step 1: Get the next available paramId
get_url = f"{domain}/api/v1/Rules/parameters/nextAvailableId"
try:
    response = requests.get(get_url)
    response.raise_for_status()
    param_id = response.json().get("paramId")
except Exception as e:
    print("Failed to retrieve paramId.")
    print("Error:", e)
    exit(1)

if not param_id:
    print("paramId not found in response.")
    print("Response:", response.text)
    exit(1)

print(f"Retrieved paramId: {param_id}")

# Step 2: Construct the POST request
post_url = f"{domain}/api/v1/Rules/parameters/parameter?paramId={param_id}"
payload = {
    "Description": param_name,
    "DataType": data_type,
    "Print": param_name
}
headers = {
    "Content-Type": "application/json"
}

try:
    post_response = requests.post(post_url, headers=headers, data=json.dumps(payload))
    post_response.raise_for_status()
    print("Parameter created successfully!")
    print("Response:", post_response.text)
except Exception as e:
    print("Failed to create parameter.")
    print("Error:", e)