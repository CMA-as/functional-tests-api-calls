import requests
from datetime import datetime
from Logger import Logger
import sys

LOGS_FOLDER = "logs/"
now_formatted = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

sys.stdout = Logger(f'{LOGS_FOLDER}Search of Parameters by Description - {now_formatted}.log')

print(f"Hello! Let's find the parameter you are looking for 🔎")
print("I will need some information about the parameter and the API")

domain = input("🌍 Enter the domain of the API (Press Enter for https://digistat.sasicu.ascom-demo.local): ").strip()
domain = "https://digistat.sasicu.ascom-demo.local" if domain.strip() == "" else domain
sys.stdout.log_user_input(domain)
title_of_parameter = input("🔎 Insert the keyword you are looking for (e.g, HR, SpO2...): ")
sys.stdout.log_user_input(title_of_parameter)

# Make the GET request
url = f"{domain}/api/v1/Configuration/parameters"
response = requests.get(url, verify=False)

if response.status_code == 200:
    print(f"🎉 Data has been successfully retrieved. Here is a snapshot:")
    data = response.json()

    # Flatten the nested parameters list
    def flatten_parameters(parameters):
        flat_list = []
        for item in parameters:
            if isinstance(item, dict):
                flat_list.append(item)
            elif isinstance(item, list):
                flat_list.extend(flatten_parameters(item))
        return flat_list

    # Extract and flatten the parameters
    parameters = flatten_parameters(data.get("Parameters", []))

    # Total number of parameters
    total_parameters = len(parameters)

    # Filter parameters containing the keyword
    matching_parameters = [parameter for parameter in parameters if title_of_parameters.lower() in parameter.get("Description", "").lower()]

    # Number of matching parameters
    matching_count = len(matching_parameters)

    # List of matching parameter IDs
    matching_ids = [parameter["Id"] for parameter in matching_parameters]

    # Output results
    print("Total parameters:", total_parameters)
    print("Matching parameters:", matching_count)
    print("Matching parameters IDs:", matching_ids)

    export = False if input(" ✒️ Do you want me to export the parameters that match your search in a txt file? (Y/N)").strip().lower() == "n" else True

    # Write matching parameters to a text file
    if export:
        filename = f"RESULT OF SEARCH - {title_of_parameter} - {now_formatted} .txt"
        with open(filename, "w", encoding="utf-8") as file:
            for parameter in matching_parameters:
                file.write(f"Id: {parameter['Id']}, Description: {parameter['Description']}\n")
        print(f"✅ {matching_count} parameters have been successfully exported in the file {filename}")
        print("Bye bye! 😊")
    else:
        print("Ok, bye! 😊")
else:
    print(f"😭 Something went wrong... I'm sorry... Here is additional info about the issue")
    print(f"⚠️ Error code: {response.status_code}")
    print(f"{response.text}")

