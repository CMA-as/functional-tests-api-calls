#!/bin/bash

# Prompt for input
read -p "Enter the domain (e.g., https://api.example.com): " domain
read -p "Enter the parameter name: " param_name
read -p "Enter the data type (e.g., NUMERIC, STRING): " data_type

# Get the next available paramId
response=$(curl -s "$domain/api/v1/Rules/parameters/nextAvailableId")
param_id=$(echo "$response" | grep -oP '(?<="paramId": )\d+')

# Check if param_id was retrieved
if [ -z "$param_id" ]; then
  echo "Failed to retrieve paramId. Response was:"
  echo "$response"
  exit 1
fi

echo "Retrieved paramId: $param_id"

# Construct the POST request
curl -X POST "$domain/api/v1/Rules/parameters/parameter?paramId=100110" \
     -H "Content-Type: application/json" \
     -d "{\"Description\":\"$param_name\",\"DataType\":\"$data_type\",\"Print\":\"$param_name\"}"
