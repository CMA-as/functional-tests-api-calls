import requests
from datetime import datetime
from Logger import Logger
import sys

LOGS_FOLDER = "logs/"
now_formatted = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

sys.stdout = Logger(f'{LOGS_FOLDER}Search of Rule by ID - {now_formatted}.log')

print(f"Hello! Let's find the rule you are looking for 🔎")
print("I will need some information about the rule and the API")

domain = input("🌍 Enter the domain of the API (Press Enter for https://digistat.sasicu.ascom-demo.local): ").strip()
domain = "https://digistat.sasicu.ascom-demo.local" if domain.strip() == "" else domain
sys.stdout.log_user_input(domain)
guid_of_rule = input("🔎 Insert the GUID of the Rule you are looking for: ").strip()
sys.stdout.log_user_input(guid_of_rule)

# Make the GET request
url = f"{domain}/api/v1/Rules/rule?ruleId={guid_of_rule}"
response = requests.get(url, verify=False)

if response.status_code == 200:
    print(f"🎉 Data has been successfully retrieved.")
    data = response.json()

    # Flatten the nested Rules list
    def flatten_rules(rules):
        flat_list = []
        for item in rules:
            if isinstance(item, dict):
                flat_list.append(item)
            elif isinstance(item, list):
                flat_list.extend(flatten_rules(item))
        return flat_list

    # Extract and flatten the rules
    rules = flatten_rules(data.get("Rules", []))

    # Total number of rules
    total_rules = len(rules)

    if total_rules > 0:

        # Output results
        print("Matching Rules:", total_rules)

        export = False if input(" ✒️ Do you want me to export the Rules that match your search in a txt file? (Y/N)").strip().lower() == "n" else True

        # Write matching rules to a text file
        if export:
            filename = f"RESULT OF SEARCH - {guid_of_rule} - {now_formatted} .txt"
            with open(filename, "w", encoding="utf-8") as file:
                for rule in rules:
                    file.write(f"Id: {rule['Id']}, Description: {rule['Description']}\n")
            print(f"✅ {matching_count} rules have been successfully exported in the file {filename}")
            print("Bye bye! 😊")
        else:
            print("Ok, bye! 😊")

    else:
        print(f"However, no rules with the id {guid_of_rule} have been found. Sorry")
else:
    print(f"😭 Something went wrong... I'm sorry... Here is additional info about the issue")
    print(f"⚠️ Error code: {response.status_code}")
    print(f"{response.text}")