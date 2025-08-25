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
from Logger import Logger
from datetime import datetime

CLINICAL_SCENARIO = "EX-C3-1"
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
print("To begin we need the IDs of the parameters to store the following calculated parameters:\n MEWS score \n MEWS attribute of HR \n MEWS attribute of RR \n MEWS attribute of Temp \n MEWS attribute of SpO2 \n MEWS attribute of BP")

parameter_ids_to_be_created = True if input("Have you already created them? (y/n)").strip().lower() == "n" : False

if parameter_ids_to_be_created:
    print("You can create now by using the 'creationOFNewParameters.py' script. I will wait here for you 😊")
    input("Press Enter when you have created them or CTRL+X to exit")
    parameter_ids_to_be_created = False
    #TODO: add steps for creation of parameters ID
else:
    MEWS_SCORE_PARAM_ID = input("⚙️ Parameter ID of MEWS score: ").strip()
    sys.stdout.log_user_input(f"{MEWS_SCORE_PARAM_ID}") 
    ATTR_HR_PARAM_ID = input("⚙️ Parameter ID of MEWS attribute of HR: ").strip()
    sys.stdout.log_user_input(f"{ATTR_HR_PARAM_ID}")  
    ATTR_RR_PARAM_ID = input("⚙️ Parameter ID of MEWS attribute of RR: ").strip()
    sys.stdout.log_user_input(f"{ATTR_RR_OhPARAM_ID}")  
    ATTR_TEMP_PARAM_ID = input("⚙️ Parameter ID of MEWS attribute of Temp: ").strip()
    sys.stdout.log_user_input(f"{ATTR_TEMP_PARAM_ID}") 
    ATTR_SPO2_PARAM_ID = input("⚙️ Parameter ID of MEWS attribute of SpO2: ").strip()
    sys.stdout.log_user_input(f"{ATTR_SPO2_PARAM_ID}")  
    ATTR_BP_PARAM_ID = input("⚙️ Parameter ID of MEWS attribute of BP: ").strip()
    sys.stdout.log_user_input(f"{ATTR_BP_PARAM_ID}") 

print("\nThank you! I have everything that I need now 😊. \nI will keep you updated about the steps that I am doing\n")

#TODO: complete with the following steps of rule creation and upload