"""
Processing & Filtering 

Processing:  

Set Param 80054 = Riemann integral (SpO2, 94 (threshold), over the last 60 seconds) 

IF (Param 3001 < 20)  
THEN Generate Advisory (“Clinical deterioration: SpO2 dip”, MEDIUM PRIORITY) 

 

Set Param 3002 = Riemann integral (SpO2, 94 (threshold), over the last 300 seconds) 

IF (Param 3002 < 60)  
THEN Generate Advisory (“Clinical deterioration: SpO2 multiple dips”, HIGH PRIORITY) 

 

Filtering:  

Delay SpO2 alarm for 10 sec (no reference to Riemann integral) (assuming dip <10sec). Reason: if you do not stop a “dip” based on Riemann integral, caregiver will see this alarm, but without context of the missed previous alarms. That context is provided by the advisory.  


DOUBTS:
- only one parameter
"""

import uuid
import requests
import sys
from Logger import Logger
from datetime import datetime
import json
from parameter_ids import *

CLINICAL_SCENARIO = "EX-C3-9"
LOGS_FOLDER = "logs/"
now_formatted = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

sys.stdout = Logger(f'{LOGS_FOLDER}Creation of Rule {CLINICAL_SCENARIO} - {now_formatted}.log')

#User inserts IDs,thresholds,locations
print(f"Hello! Let's create the rule for the clinical scenario {CLINICAL_SCENARIO} 😊")
print("I will need some information about the rule and the API")
guid_rule = input("⚙️ First: are you updating an existing rule? If so, insert the guid, if not, leave empty: ") 
guid_rule = guid_rule.strip() if guid_rule.strip() == "" else uuid.uuid4()
sys.stdout.log_user_input(guid_rule)

patient_profile = input("👤 What is the patient profile associated to this configuration? (e.g 'Regular', 'Heart failure', 'Pneumonia'..) ")
sys.stdout.log_user_input(patient_profile)

SPO2_INTEGRAL_THRESHOLD = int(input("    🩺 Lower SpO2 Riemann integral threshold for this profile (e.g. 95): "))
sys.stdout.log_user_input(f"{SPO2_INTEGRAL_THRESHOLD}")
SPO2_INTEGRAL_DURATION_SECONDS = int(input("    🩺 How many seconds should the integral be calculated over? (e.g. 60): "))
sys.stdout.log_user_input(f"{SPO2_INTEGRAL_DURATION_SECONDS}")
ADVISORY_INTEGRAL_TRIGGER = int(input("    🩺 What threshold of the integral should trigger the multiple spO2 dips advisory? (e.g. 20): "))
sys.stdout.log_user_input(f"{ADVISORY_INTEGRAL_TRIGGER}")
ADVISORY_PRIORITY = int(input("    🩺 What is the priority of the Advisory of multiple spO2 dips? (e.g. 2): "))
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


#Get parameter IDs or create new ones
print(f"To begin we need the IDs of the parameter to store the following calculated parameter:\n SpO2 Riemann Integral of the last {SPO2_INTEGRAL_DURATION_SECONDS} seconds")

parameter_ids_to_be_created = True if input("Have you already created them? (y/n)").strip().lower() == "n" else False

if parameter_ids_to_be_created:
    print("You can create now by using the 'creationOFNewParameters.py' script. I will wait here for you 😊")
    input("Press Enter when you have created them or CTRL+X to exit")
    parameter_ids_to_be_created = False

SPO2_INTEGRAL_PARAM_ID = input(f"⚙️ Parameter ID of SpO2 Riemann integral over {SPO2_INTEGRAL_DURATION_SECONDS} seconds: ").strip()
sys.stdout.log_user_input(f"{SPO2_INTEGRAL_PARAM_ID}") 

print("\nThank you! I have everything that I need now 😊. \nI will keep you updated about the steps that I am doing\n")

#Creation and validation of expressions
input("STEP 1 : Creation of expressions\n")
INTEGRAL_EXPRESSION = f"Integral({SPO2_PARAM_ID},{SPO2_INTEGRAL_DURATION_SECONDS},{SPO2_INTEGRAL_THRESHOLD},true,2)"
ADVISORY_GENERATION_EXPRESSION = f"Advisory(( #{SPO2_INTEGRAL_PARAM_ID} < {ADVISORY_INTEGRAL_TRIGGER}),'EX-C3-9-multiplespo2dips',{ADVISORY_PRIORITY},'Multiple SpO2 dips in the last {SPO2_INTEGRAL_DURATION_SECONDS} seconds detected')"


print(f"    These are the expressions that I will use: \n")
print(f"    Calculation Riemann Integral SpO2: {INTEGRAL_EXPRESSION}")
print(f"    Advisory: {ADVISORY_GENERATION_EXPRESSION}")

input("STEP 2 : Creation of the formulas\n")

formula_integral_spo2 =  { 
        "Expression": INTEGRAL_EXPRESSION, 
        "OutputParamId": SPO2_INTEGRAL_PARAM_ID, 
        "OutputUnitId": 8, 
        "ValidityQuantThreashold": 0, 
        "ValiditySpreadThreashold": 0, 
        "DecimalPosition": 2, 
    } 

formula_advisory =  { 
        "Expression": ADVISORY_GENERATION_EXPRESSION, 
        "OutputParamId": 0, 
        "OutputUnitId": 8, 
        "ValidityQuantThreashold": 0, 
        "ValiditySpreadThreashold": 0, 
        "DecimalPosition": 2, 
    }  

print("    These are the formulas that we will use\n")
print(f"    {formula_integral_spo2}\n")
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
    formula_integral_spo2,
    formula_advisory
] 
}

print("    This is the rule that we will use")
print(f"    {rule}\n")

#POST request
input("STEP 4 : Let's upload that! \n")
url = f"{domain}/api/v1/Rules/rule?ruleId={guid_rule}"
response = requests.post(url, json=rule, verify=False)


if response.status_code == 200:
    print(f"🎉 NICE! The rule {guid_rule} has been successfully uploaded")
else:
    print(f"😭 Something went wrong... I'm sorry... Here is additional info about the issue")
    print(f"⚠️ Error code: {response.status_code}")
    print(f"{response.text}")