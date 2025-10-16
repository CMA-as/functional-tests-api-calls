"""
Processing: 

Calculate MEWS 

Set Param 5001 = latest value of MEWS 

Set Param 5002 = attribute of HR in MEWS 

Set Param 5003 = attribute of RR in MEWS 

Set Param 5004 = attribute of Temp in MEWS 

Set Param 5005 = attribute of SpO2 in MEWS 

Set Param 5006 = attribute of BP in MEWS 

 

If (Param 5001) > 5 AND (Param 5002)>2 AND (Param 5003)>2 AND (Param 5006)>2 

THEN Generate Advisory (“MEWS Advisory with overall score, the attributes of the score and the possible complication = Heart Failure”, MEDIUM PRIORITY) 

 


If (Param 5001) > 5 AND (Param 5002)>2 AND (Param 5003)>2 AND (Param 5004)>2 
THEN Generate Advisory (“MEWS Advisory with overall score, the attributes of the score and the possible complication = Pneumonia”, MEDIUM PRIORITY) 

"""

import uuid
import requests
import sys
import json
from Logger import Logger
from datetime import datetime
from parameter_ids import *
from support_functions import *

CLINICAL_SCENARIO = "EX-C3-1"
LOGS_FOLDER = "logs/"
now_formatted = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

sys.stdout = Logger(f'{LOGS_FOLDER}Creation of Rule {CLINICAL_SCENARIO} - {now_formatted}.log')

#User inserts IDs,thresholds,locations
print(f"Hello! Let's create the rule for the clinical scenario {CLINICAL_SCENARIO} 😊")
print("I will need some information about the rule and the API")

guid_rule = config_guid_rule()
sys.stdout.log_user_input(str(guid_rule))

patient_profile = config_patient_profile()
sys.stdout.log_user_input(patient_profile)


MEWS_LOWER_THRESHOLD = int(input("    🩺 Lower MEWS score threshold for this profile (e.g. 5): "))
sys.stdout.log_user_input(f"{MEWS_LOWER_THRESHOLD}")
HR_ATTR_LOWER_THRESHOLD = int(input("    🩺 Lower HR attribute score threshold for this profile (e.g. 2): "))
sys.stdout.log_user_input(f"{HR_ATTR_LOWER_THRESHOLD}")
RR_ATTR_LOWER_THRESHOLD = int(input("    🩺 Lower RR attribute score threshold for this profile (e.g. 2): "))
sys.stdout.log_user_input(f"{RR_ATTR_LOWER_THRESHOLD}")
TEMP_ATTR_LOWER_THRESHOLD = int(input("    🩺 Lower Temp attribute score threshold for this profile (e.g. 2): "))
sys.stdout.log_user_input(f"{TEMP_ATTR_LOWER_THRESHOLD}")
SPO2_ATTR_LOWER_THRESHOLD = int(input("    🩺 Lower SpO2 attribute score threshold for this profile (e.g. 2): "))
sys.stdout.log_user_input(f"{SPO2_ATTR_LOWER_THRESHOLD}")
BP_ATTR_LOWER_THRESHOLD = int(input("    🩺 Lower BP attribute score threshold for this profile (e.g. 2): "))
sys.stdout.log_user_input(f"{BP_ATTR_LOWER_THRESHOLD}")

title_of_rule = config_title_of_rule(CLINICAL_SCENARIO,patient_profile)
sys.stdout.log_user_input(title_of_rule)

locations = config_bed_locations()
sys.stdout.log_user_input(str(locations))

stop_at_first_exception = config_stops_on_exception()
sys.stdout.log_user_input(str(stop_at_first_exception))

domain = config_api_domain()
sys.stdout.log_user_input(domain)

#Get parameter IDs or create new ones
print("To begin we need the IDs of the parameters to store the following calculated parameters:\n MEWS score \n MEWS attribute of HR \n MEWS attribute of RR \n MEWS attribute of Temp \n MEWS attribute of SpO2 \n MEWS attribute of BP")

parameter_ids_to_be_created = True if input("Have you already created them? (y/n)").strip().lower() == "n" else False

if parameter_ids_to_be_created:
    print("You can create now by using the 'creationOFNewParameters.py' script. I will wait here for you 😊")
    input("Press Enter when you have created them or CTRL+X to exit")
    parameter_ids_to_be_created = False
    

MEWS_SCORE_PARAM_ID = input("⚙️ Parameter ID of MEWS score: ").strip()
sys.stdout.log_user_input(f"{MEWS_SCORE_PARAM_ID}") 
ATTR_HR_PARAM_ID = input("⚙️ Parameter ID of MEWS attribute of HR: ").strip()
sys.stdout.log_user_input(f"{ATTR_HR_PARAM_ID}")  
ATTR_RR_PARAM_ID = input("⚙️ Parameter ID of MEWS attribute of RR: ").strip()
sys.stdout.log_user_input(f"{ATTR_RR_PARAM_ID}")  
ATTR_TEMP_PARAM_ID = input("⚙️ Parameter ID of MEWS attribute of Temp: ").strip()
sys.stdout.log_user_input(f"{ATTR_TEMP_PARAM_ID}") 
ATTR_SPO2_PARAM_ID = input("⚙️ Parameter ID of MEWS attribute of SpO2: ").strip()
sys.stdout.log_user_input(f"{ATTR_SPO2_PARAM_ID}")  
ATTR_BP_PARAM_ID = input("⚙️ Parameter ID of MEWS attribute of BP: ").strip()
sys.stdout.log_user_input(f"{ATTR_BP_PARAM_ID}") 

print("\nThank you! I have everything that I need now 😊. \nI will keep you updated about the steps that I am doing\n")

#Creation and validation of expressions
input("STEP 1 : Creation of expressions\n")

ATTR_RR_EXPRESSION = f"If(#{RR_PARAM_ID} <= 8, 1, If(#{RR_PARAM_ID} <= 11, 1, If(#{RR_PARAM_ID} <= 20, 0, If(#{RR_PARAM_ID} <= 24, 2, 3))))"
ATTR_SPO2_EXPRESSION = f"If(#{SPO2_PARAM_ID} <= 91, 3, If(#{SPO2_PARAM_ID} <= 93, 2, If(#{SPO2_PARAM_ID} <= 95, 1, 0)))"
ATTR_TEMP_EXPRESSION = f"If(#{TEMP_PARAM_ID} <= 35.0, 3, If(#{TEMP_PARAM_ID} <= 36.0, 1, If(#{TEMP_PARAM_ID} <= 38.0, 0, If(#{TEMP_PARAM_ID} <= 39.0, 1, 2))))"
ATTR_BP_EXPRESSION = f"If(#{ABP_SYS_PARAM_ID} <= 90, 3, If(#{ABP_SYS_PARAM_ID} <= 100, 2, If(#{ABP_SYS_PARAM_ID} <= 110, 1, 0)))"
ATTR_HR_EXPRESSION = f"If(#{HR_PARAM_ID} <= 40, 3, If(#{HR_PARAM_ID} <= 50, 1, If(#{HR_PARAM_ID} <= 90, 0, If(#{HR_PARAM_ID} <= 100, 1, If(#{HR_PARAM_ID} <= 130, 2, 3)))))"
MEWS_SCORE_EXPRESSION = f"#{ATTR_RR_PARAM_ID} + #{ATTR_SPO2_PARAM_ID} + #{ATTR_TEMP_PARAM_ID} + #{ATTR_BP_PARAM_ID} + #{ATTR_HR_PARAM_ID}"
ADVISORY_GENERATION_EXPRESSION = f"Advisory((#{MEWS_SCORE_PARAM_ID} > 5 AND #{ATTR_HR_PARAM_ID} > 2 AND #{ATTR_RR_PARAM_ID} > 2 AND #{ATTR_BP_PARAM_ID} > 2) OR (#{MEWS_SCORE_PARAM_ID} > 5 AND #{ATTR_HR_PARAM_ID} > 2 AND #{ATTR_RR_PARAM_ID} > 2 AND #{ATTR_TEMP_PARAM_ID} > 2) OR (#{MEWS_SCORE_PARAM_ID} > 5), 'MEWS score '_(#{MEWS_SCORE_PARAM_ID})_' . Potential complication : '_If(#{MEWS_SCORE_PARAM_ID} > 5 AND #{ATTR_HR_PARAM_ID} > 2 AND #{ATTR_RR_PARAM_ID} > 2 AND #{ATTR_BP_PARAM_ID} > 2, 'Heart Failure', If(#{MEWS_SCORE_PARAM_ID} > 5 AND #{ATTR_HR_PARAM_ID} > 2 AND #{ATTR_RR_PARAM_ID} > 2 AND #{ATTR_TEMP_PARAM_ID} > 2, 'Pneumonia', '')), 2, 'MEWS score '_(#{MEWS_SCORE_PARAM_ID})_' . Potential complication : '_If(#{MEWS_SCORE_PARAM_ID} > 5 AND #{ATTR_HR_PARAM_ID} > 2 AND #{ATTR_RR_PARAM_ID} > 2 AND #{ATTR_BP_PARAM_ID} > 2, 'Heart Failure', If(#{MEWS_SCORE_PARAM_ID} > 5 AND #{ATTR_HR_PARAM_ID} > 2 AND #{ATTR_RR_PARAM_ID} > 2 AND #{ATTR_TEMP_PARAM_ID} > 2, 'Pneumonia', '')))"
ADVISORY_GENERATION_EXPRESSION = ADVISORY_GENERATION_EXPRESSION = f"Advisory((#{MEWS_SCORE_PARAM_ID} > 5 AND #{ATTR_HR_PARAM_ID} > 2 AND #{ATTR_RR_PARAM_ID} > 2 AND #{ATTR_BP_PARAM_ID} > 2) OR (#{MEWS_SCORE_PARAM_ID} > 5 AND #{ATTR_HR_PARAM_ID} > 2 AND #{ATTR_RR_PARAM_ID} > 2 AND #{ATTR_TEMP_PARAM_ID} > 2) OR (#{MEWS_SCORE_PARAM_ID} > 5),'MEWS score '_(#{MEWS_SCORE_PARAM_ID})_' . Potential complication : '_If(#{MEWS_SCORE_PARAM_ID} > 5 AND #{ATTR_HR_PARAM_ID} > 2 AND #{ATTR_RR_PARAM_ID} > 2 AND #{ATTR_TEMP_PARAM_ID} > 2,'Pneumonia',If(#{MEWS_SCORE_PARAM_ID} > 5 AND #{ATTR_HR_PARAM_ID} > 2 AND #{ATTR_RR_PARAM_ID} > 2 AND #{ATTR_BP_PARAM_ID} > 2,'Heart Failure','')),2,'MEWS score '_(#{MEWS_SCORE_PARAM_ID})_' . Potential complication : '_If(#{MEWS_SCORE_PARAM_ID} > 5 AND #{ATTR_HR_PARAM_ID} > 2 AND #{ATTR_RR_PARAM_ID} > 2 AND #{ATTR_TEMP_PARAM_ID} > 2,'Pneumonia',If(#{MEWS_SCORE_PARAM_ID} > 5 AND #{ATTR_HR_PARAM_ID} > 2 AND #{ATTR_RR_PARAM_ID} > 2 AND #{ATTR_BP_PARAM_ID} > 2,'Heart Failure','')))"

"""

If(
  MEWS > 5 AND SpO₂ > 2 AND RR > 2 AND BP > 2 → "Pneumonia",
  Else If MEWS > 5 AND SpO₂ > 2 AND RR > 2 AND HR > 2 → "Heart Failure",
  Else → ""
)

"""


print(f"    These are the expressions that I will use: \n")
print(f"    Calculation RR MEWS attribute: {ATTR_RR_EXPRESSION}")
print(f"    Calculation SPO2 MEWS attribute: {ATTR_SPO2_EXPRESSION}")
print(f"    Calculation TEMP MEWS attribute: {ATTR_TEMP_EXPRESSION}")
print(f"    Calculation BP MEWS attribute: {ATTR_BP_EXPRESSION}")
print(f"    Calculation HR MEWS attribute: {ATTR_HR_EXPRESSION}")
print(f"    Calculation of MEWS score: {MEWS_SCORE_EXPRESSION}")
print(f"    Advisory: {ADVISORY_GENERATION_EXPRESSION}")

input("STEP 2 : Creation of the formulas\n")

formula_rr_attr =  { 
        "Expression": ATTR_RR_EXPRESSION, 
        "OutputParamId": ATTR_RR_PARAM_ID, 
        "OutputUnitId": 8, 
        "ValidityQuantThreashold": 0, 
        "ValiditySpreadThreashold": 0, 
        "DecimalPosition": 2, 
    } 

formula_spo2_attr =  { 
        "Expression": ATTR_SPO2_EXPRESSION, 
        "OutputParamId": ATTR_SPO2_PARAM_ID, 
        "OutputUnitId": 8, 
        "ValidityQuantThreashold": 0, 
        "ValiditySpreadThreashold": 0, 
        "DecimalPosition": 2, 
    } 

formula_temp_attr =  { 
        "Expression": ATTR_TEMP_EXPRESSION, 
        "OutputParamId": ATTR_TEMP_PARAM_ID, 
        "OutputUnitId": 8, 
        "ValidityQuantThreashold": 0, 
        "ValiditySpreadThreashold": 0, 
        "DecimalPosition": 2, 
    } 

formula_bp_attr =  { 
        "Expression": ATTR_BP_EXPRESSION, 
        "OutputParamId": ATTR_BP_PARAM_ID, 
        "OutputUnitId": 8, 
        "ValidityQuantThreashold": 0, 
        "ValiditySpreadThreashold": 0, 
        "DecimalPosition": 2, 
    } 

formula_hr_attr =  { 
        "Expression": ATTR_HR_EXPRESSION, 
        "OutputParamId": ATTR_HR_PARAM_ID, 
        "OutputUnitId": 8, 
        "ValidityQuantThreashold": 0, 
        "ValiditySpreadThreashold": 0, 
        "DecimalPosition": 2, 
    } 

formula_mews_score =  { 
        "Expression": MEWS_SCORE_EXPRESSION, 
        "OutputParamId": MEWS_SCORE_PARAM_ID, 
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
print(f"    {formula_rr_attr}\n")
print(f"    {formula_spo2_attr}\n")
print(f"    {formula_hr_attr}\n")
print(f"    {formula_temp_attr}\n")
print(f"    {formula_bp_attr}\n")
print(f"    {formula_mews_score}\n")
print(f"    {formula_advisory}\n")

#Creation of rule
input("STEP 3 : Creation of the rule\n")


rule = { 
"Description": title_of_rule, 
"Locations": locations, 
"StopAtFirstException": stop_at_first_exception, 
"Formulas": [ 
    formula_rr_attr,
    formula_spo2_attr,
    formula_temp_attr,
    formula_bp_attr,
    formula_hr_attr,
    formula_mews_score,
    formula_advisory
] 
}

print("    This is the rule that we will use")
print(json.dumps(rule, indent=4))

#POST request
input("STEP 4 : Let's upload that! \n")

response = upload_rule(domain,guid_rule,rule)

if response.status_code == 200:
    print(f"🎉 NICE! The rule {guid_rule} has been successfully uploaded")
else:
    print(f"😭 Something went wrong... I'm sorry... Here is additional info about the issue")
    print(f"⚠️ Error code: {response.status_code}")
    print(f"{response.text}")


print("The logs have been saved in the 'logs' folder")
input("Have a nice day! ✨ (Press Enter to close)")