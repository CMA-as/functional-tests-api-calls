import uuid
import requests

def config_guid_rule():
    guid_rule = input("⚙️ First: are you updating an existing rule? If so, insert the guid, if not, leave empty: ") 
    guid_rule = guid_rule.strip() if len(guid_rule.strip()) > 0 else uuid.uuid4()
    return guid_rule

def config_patient_profile():
    patient_profile = input("👤 What is the patient profile associated to this configuration? (e.g 'Regular', 'COPD', 'Post-operative'..) ")
    return patient_profile

def config_title_of_rule(clinical_scenario,patient_profile):
    title_of_rule = clinical_scenario + " - " + patient_profile + " - " + input(f"✒️ What name do you want to give to the rule? (Keep in mind that the name will start with {clinical_scenario} - {patient_profile} ):")
    return title_of_rule

def config_bed_locations():
    beds_string = input("🛌 Beds on which the rule has to run (if more than one, divide the numbers with a comma): ")
    locations = [str(item.strip()) for item in beds_string.split(",") if item.strip()]
    return locations

def config_stops_on_exception():
    stop_at_first_exception_string = input("❓ Do you want the rule to stop if one of the expressions raise an error? (Type Y or N): ")
    stop_at_first_exception = False if stop_at_first_exception_string.lower() == "n" else True
    return stop_at_first_exception

def config_api_domain():
    domain = input("🌍 Enter the domain of the API (Press Enter for https://digistat.sasicu.ascom-demo.local): ").strip()
    domain = "https://digistat.sasicu.ascom-demo.local" if domain.strip() == "" else domain
    return domain

def upload_rule(domain,guid_rule,rule):
    url = f"{domain}/api/v1/Rules/rules/rule?ruleId={guid_rule}"

    response = requests.post(url, json=rule, verify=False) 

    print(f"    URL: {url}")
    print("    JSON payload:")
    print(json.dumps(rule, indent=4))

    return response