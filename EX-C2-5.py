
"""
Processing:  

Set Param 2001 = last value of HR 

Set Param 3029 = last value of ABP 

IF ((Param 2001) > upper range 1 OR (Param 2001) < lower range 1) AND 
((Param 3029) > upper range 2 OR (Param 3029) < lower range 2) 
THEN Generate Advisory (“message of advisory”, MEDIUM PRIORITY) 

"""


import uuid
import requests
import sys
from Logger import Logger
from datetime import datetime


HR_PARAM_ID = 2001
ABP_PARAM_ID = 3029
HR_LOWER_THRESHOLD = 40
HR_UPPER_THRESHOLD = 120
ABP_LOWER_THRESHOLD = 40
ABP_UPPER_THRESHOLD = 120

CLINICAL_SCENARIO = "EX-C2-5"
LOGS_FOLDER = "logs/"
now_formatted = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")


sys.stdout = Logger(f'{LOGS_FOLDER}Creation of Rule {CLINICAL_SCENARIO} - {now_formatted}.log')

#User inserts IDs,thresholds,locations
print(f"Hello! Let's create the rule for the clinical scenario {CLINICAL_SCENARIO} 😊")
print("I will need some information about the rule and the API")
guid_rule = input("⚙️ First: are you updating an existing rule? If so, insert the guid, if not, leave empty: ") 
guid_rule = guid_rule.strip() if guid_rule.strip() == "" else uuid.uuid4()
sys.stdout.log_user_input(guid_rule)


patient_profile = input("👤 What is the patient profile associated to this configuration? (e.g 'Regular', 'COPD', 'Post-operative'..) ")
sys.stdout.log_user_input(patient_profile)
HR_LOWER_THRESHOLD = int(input("    🩺 Lower HR threshold for this profile (e.g. 40): "))
sys.stdout.log_user_input(f"{HR_LOWER_THRESHOLD}")
HR_UPPER_THRESHOLD = int(input("    🩺 Upper HR threshold for this profile (e.g. 120): "))
sys.stdout.log_user_input(f"{HR_UPPER_THRESHOLD}")
ABP_LOWER_THRESHOLD = int(input("    🩺 Lower ABP threshold for this profile (e.g. 60): "))
sys.stdout.log_user_input(f"{ABP_LOWER_THRESHOLD}")
ABP_UPPER_THRESHOLD = int(input("    🩺 Upper ABP threshold for this profile (e.g. 140): "))
sys.stdout.log_user_input(f"{ABP_UPPER_THRESHOLD}")

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

#Creation and validation of expressions
print("STEP 1 : Creation of expression\n")
expression = f"Advisory((#{HR_PARAM_ID} > {HR_UPPER_THRESHOLD} OR #{HR_PARAM_ID}<{HR_LOWER_THRESHOLD} ) AND (#{ABP_PARAM_ID} > {ABP_UPPER_THRESHOLD} OR #{ABP_PARAM_ID} < {ABP_LOWER_THRESHOLD}),'message of advisory',  2,'message of advisory')"
print(f"    This is the expression that I will use: ")
print(f"    {expression}\n")

#check_correctness(expression)

#Creation of formula
print("STEP 2 : Creation of the formula\n")

formula =  { 
        "Expression": expression, 
        "OutputParamId": 0, 
        "OutputUnitId": 8, 
        "ValidityQuantThreashold": 0, 
        "ValiditySpreadThreashold": 0, 
        "DecimalPosition": 2, 
    } 

print("    This is the formula that we will use")
print(f"    {formula}\n")

#Creation of rule
print("STEP 3 : Creation of the rule\n")

description = title_of_rule
locations = [int(item.strip()) for item in beds_string.split(",")]
stop_at_first_exception = False if stop_at_first_exception_string.lower() == "n" else True

rule = { 
"Description": description, 
"Locations": locations, 
"StopAtFirstException": stop_at_first_exception, 
"Formulas": [ 
    formula
] 
}

print("    This is the rule that we will use")
print(f"    {rule}\n")

#POST request
print("STEP 4 : Let's upload that! \n")
url = f"{domain}/api/v1/Rules/rule?ruleId={guid_rule}"
response = requests.post(url, json=rule, verify=False)


if response.status_code == 200:
    print(f"🎉 NICE! The rule {guid_rule} has been successfully uploaded")
else:
    print(f"😭 Something went wrong... I'm sorry... Here is additional info about the issue")
    print(f"⚠️ Error code: {response.status_code}")
    print(f"{response.text}")
