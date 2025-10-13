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