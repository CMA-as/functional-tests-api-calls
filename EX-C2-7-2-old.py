"""
Processing & Filtering 

 

Select COPD patient profile, with associated changes in “normal” values: 

SpO2 < 100 should be changed to SpO2 < 90 (values below 100, but above 90 are accepted) 

Resp. Rate > 12 should be changed to Resp. Rate > 15 (values above 12, but below 15 are accepted 

 

Processing: 

Set Param 7501 = latest value of SpO2 

Set Param 4004 = latest value of Resp. Rate 

 

Filtering: 

Trigger of the workflow: SpO2 low alarm  

If (Param 7501) < 90 

THEN Send out alarm 

ELSE Stop alarm 

 

Trigger of the workflow: RR high alarm  

If (Param 3003) > 15 

THEN Send out alarm 
ELSE Stop alarm 

text to be updated by Jeroen, as it is based on an advisory generated based on the spo2 level
"""

import uuid
import requests
import sys
from Logger import Logger
from datetime import datetime
import json
from parameter_ids import *

CLINICAL_SCENARIO = "EX-C2-7-2"
LOGS_FOLDER = "logs/"
now_formatted = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

sys.stdout = Logger(f'{LOGS_FOLDER}Creation of Rule {CLINICAL_SCENARIO} - {now_formatted}.log')

#User inserts IDs,thresholds,locations
print(f"Hello! Let's create the rule for the clinical scenario {CLINICAL_SCENARIO} 😊")
print("I will need some information about the rule and the API")
guid_rule = input("⚙️ First: are you updating an existing rule? If so, insert the guid, if not, leave empty: ") 
guid_rule = guid_rule.strip() if guid_rule.strip() == "" else uuid.uuid4()
sys.stdout.log_user_input(guid_rule)

patient_profile = input("👤 What is the patient profile associated to this configuration? (e.g 'Regular', 'COPD', ..) ")
sys.stdout.log_user_input(patient_profile)

ADVISORY_TRIGGER = int(input("    🩺 What value of Sp02 should trigger the advisory? (e.g. 90): "))
sys.stdout.log_user_input(f"{ADVISORY_TRIGGER}")
ADVISORY_PRIORITY = int(input("    🩺 What is the priority of the Advisory of low Sp=2? (e.g. 3): "))
sys.stdout.log_user_input(f"{ADVISORY_PRIORITY}")

title_of_rule = CLINICAL_SCENARIO + " - " + patient_profile + " - " + input(f"✒️ What name do you want to give to the rule? (Keep in mind that the name will start with {CLINICAL_SCENARIO} - {patient_profile} ):")
sys.stdout.log_user_input(title_of_rule)

beds_string = input("🛌 Beds on which the rule has to run (if more than one, divide the numbers with a comma): ")
sys.stdout.log_user_input(beds_string)

stop_at_first_exception_string = input("❓ Do you want the rule to stop if one of the expressions raise an error? (Type Y or N): ")
sys.stdout.log_user_input(stop_at_first_exception_string)

domain = input("🌍 Enter the domain of the API (Press Enter for https://digistat.sasicu.ascom-demo.local): ").strip()
domain = "https://digistat.sasicu.ascom-demo.local" if domain.strip() == "" else domain
sys.stdout.log_user_input(domain)

print("\nThank you! I have everything that I need now 😊. \nI will keep you updated about the steps that I am doing\n")

#to do Chiara, check
guid_rule=uuid.uuid4()

#Creation and validation of expressions
input("STEP 1 : Creation of expressions\n")

ADVISORY_GENERATION_EXPRESSION = f"Advisory(( #{SPO2_PARAM_ID} < {ADVISORY_TRIGGER}),'EX-C2-7-2-lowspO2',{ADVISORY_PRIORITY},'Low SpO2 detected')"

print(f"    These are the expressions that I will use: \n")
print(f"    Advisory: {ADVISORY_GENERATION_EXPRESSION}")

input("STEP 2 : Creation of the formulas\n")

formula_advisory =  { 
        "Expression": ADVISORY_GENERATION_EXPRESSION, 
        "OutputParamId": 0, 
        "OutputUnitId": 8, 
        "ValidityQuantThreashold": 0, 
        "ValiditySpreadThreashold": 0, 
        "DecimalPosition": 2, 
    }  

print("    These are the formulas that we will use\n")
print(f"    {formula_advisory}\n")

#Creation of rule
input("STEP 3 : Creation of the rule\n")

description = title_of_rule
locations = [int(item.strip()) for item in beds_string.split(",")]
stop_at_first_exception = False if stop_at_first_exception_string.lower() == "n" else True

rule = { 
"Description": description, 
"Locations": locations, 
"StopAtFirstException": stop_at_first_exception, 
"Formulas": [ 
    formula_advisory
] 
}

print("    This is the rule that we will use")
print(f"    {rule}\n")

#POST request
input("STEP 4 : Let's upload that! \n")
url = f"{domain}/api/v1/Rules/rules/rule?ruleId={guid_rule}"
input(f"{url}")
response = requests.post(url, json=rule, verify=False)
input(f"{response}")

if response.status_code == 200:
    print(f"🎉 NICE! The rule {guid_rule} has been successfully uploaded")
else:
    print(f"😭 Something went wrong... I'm sorry... Here is additional info about the issue")
    print(f"⚠️ Error code: {response.status_code}")
    print(f"{response.text}")