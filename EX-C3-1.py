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