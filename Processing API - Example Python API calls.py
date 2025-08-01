import http.client
import json


###Get alla parameters
conn = http.client.HTTPConnection("127.0.0.1", 8088)
payload = ''
headers = {}
conn.request("GET", "/api/v1/Configuration/parameters", payload, headers)
res = conn.getresponse()
data = res.read()
print(data.decode("utf-8"))

###Get Next Parameter ID
conn = http.client.HTTPConnection("127.0.0.1", 8088)
payload = ''
headers = {}
conn.request("GET", "/api/v1/Rules/parameters/nextId", payload, headers)
res = conn.getresponse()
data = res.read()
print(data.decode("utf-8"))

###Create output parameter
conn = http.client.HTTPConnection("127.0.0.1", 8088)
payload = json.dumps({
  "Description": "Param Test",
  "DataType": "NUMERIC",
  "Print": "Param Test"
})
headers = {
  'Content-Type': 'application/json'
}
conn.request("POST", "/api/v1/Rules/parameters/parameter?paramId=100004", payload, headers)
res = conn.getresponse()
data = res.read()
print(data.decode("utf-8"))

###Update output parameter
conn = http.client.HTTPConnection("127.0.0.1", 8088)
payload = json.dumps({
  "Description": "Param HR Avg Test Updated",
  "DataType": "NUMERIC",
  "Print": "Param HR Avg Test Updated"
})
headers = {
  'Content-Type': 'application/json'
}
conn.request("POST", "/api/v1/Rules/parameters/parameter?paramId=100004", payload, headers)
res = conn.getresponse()
data = res.read()
print(data.decode("utf-8"))

###Get Units List
conn = http.client.HTTPConnection("127.0.0.1", 8088)
payload = ''
headers = {}
conn.request("GET", "/api/v1/Configuration/units", payload, headers)
res = conn.getresponse()
data = res.read()
print(data.decode("utf-8"))

###Create Rule
conn = http.client.HTTPConnection("127.0.0.1", 8088)
payload = json.dumps({
  "Description": "Test Avg rule",
  "StopAtFirstException": True,
  "Locations": [
    "1"
  ],
  "Formulas": [
    {
      "Expression": "Avg(2001,60)",
      "OutputParamId": 100004,
      "OutputUnitId": 8,
      "ValidityQuantThreashold": 0,
      "ValiditySpreadThreashold": 0,
      "DecimalPosition": 2
    }
  ]
})
headers = {
  'Content-Type': 'application/json'
}
conn.request("POST", "/api/v1/Rules/rules/rule?ruleId=544ddbe8-b279-44fa-baf2-7c7afe260036", payload, headers)
res = conn.getresponse()
data = res.read()
print(data.decode("utf-8"))

###Update Rule
conn = http.client.HTTPConnection("127.0.0.1", 8088)
payload = json.dumps({
  "Description": "Test avg rule updated",
  "StopAtFirstException": True,
  "Locations": [
    "1"
  ],
  "Formulas": [
    {
      "Expression": "Avg(2001,60) - 40",
      "OutputParamId": 100004,
      "OutputUnitId": 8,
      "ValidityQuantThreashold": 0,
      "ValiditySpreadThreashold": 0,
      "DecimalPosition": 2
    }
  ]
})
headers = {
  'Content-Type': 'application/json'
}
conn.request("POST", "/api/v1/Rules/rules/rule?ruleId=544ddbe8-b279-44fa-baf2-7c7afe260036", payload, headers)
res = conn.getresponse()
data = res.read()
print(data.decode("utf-8"))

###Get created Rule
conn = http.client.HTTPConnection("127.0.0.1", 8088)
payload = ''
headers = {}
conn.request("GET", "/api/v1/Rules/rules/rule?ruleId=544ddbe8-b279-44fa-baf2-7c7afe260036", payload, headers)
res = conn.getresponse()
data = res.read()
print(data.decode("utf-8"))


###Get running Rules dataset
conn = http.client.HTTPConnection("127.0.0.1", 8088)
payload = ''
headers = {}
conn.request("GET", "/dataset/Get", payload, headers)
res = conn.getresponse()
data = res.read()
print(data.decode("utf-8"))