import requests
from datetime import datetime
import os

# Set user's personal details
GENDER = "YOUR GENDER"
WEIGHT_KG = YOUR WEIGHT
HEIGHT_CM = YOUR HEIGHT
AGE = YOUR AGE

# Retrieve app ID, API key, and Google Sheets API endpoint from environment variables
APP_ID = os.environ.get("APP_ID")
API_KEY = os.environ.get("API_KEY")
SHEET_ENDPOINT = os.environ.get("SHEET_ENDPOINT")

# Prompt user to input exercise details
exercise_text = input("Tell me which exercises you did: ")

# Set headers and parameters for Nutritionix API request
headers = {
    "x-app-id": APP_ID,
    "x-app-key": API_KEY,
}
parameters = {
    "query": exercise_text,
    "gender": GENDER,
    "weight_kg": WEIGHT_KG,
    "height_cm": HEIGHT_CM,
    "age": AGE
}

# Send POST request to Nutritionix API
response = requests.post("https://trackapi.nutritionix.com/v2/natural/exercise", json=parameters, headers=headers)
result = response.json()

# Print exercise results
print(result)

# Set date and time for exercise log entry
today_date = datetime.now().strftime("%d/%m/%Y")
now_time = datetime.now().strftime("%X")

# Loop through exercise results and send POST requests to Google Sheets API to log exercise details
for exercise in result["exercises"]:
    sheet_inputs = {
        "workout": {
            "date": today_date,
            "time": now_time,
            "exercise": exercise["name"].title(),
            "duration": exercise["duration_min"],
            "calories": exercise["nf_calories"]
        }
    }

    # Send POST request to Google Sheets API with no authentication
    sheet_response = requests.post(SHEET_ENDPOINT, json=sheet_inputs)

    # Send POST request to Google Sheets API with basic authentication
    sheet_response = requests.post(SHEET_ENDPOINT, json=sheet_inputs, auth=(os.environ.get("USERNAME"), os.environ.get("PASSWORD")))

    # Send POST request to Google Sheets API with bearer token authentication
    bearer_headers = {
        "Authorization": f"Bearer {os.environ.get('TOKEN')}"
    }
    sheet_response = requests.post(SHEET_ENDPOINT, json=sheet_inputs, headers=bearer_headers)

    # Print response from Google Sheets API
    print(sheet_response.text)
