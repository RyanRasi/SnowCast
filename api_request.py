import requests
import sys

import csv
import codecs

from dotenv import dotenv_values

# Load variables from .env file
env_vars = dotenv_values(".env")

# Access variables
API_KEY = env_vars.get("API_KEY")

API_DAY_RANGE = 365
API_LOCATION = "hopfgarten"
API_REQUEST = f"https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/{API_LOCATION}/last{API_DAY_RANGE}days?include=days&key={API_KEY}&contentType=csv"
print(API_REQUEST)

response = requests.get(API_REQUEST)
                
if response.status_code != 200:
    print('Request failed\nStatus code: ', response.status_code)
    exit()
else:
    # Save the CSV data to a file
    with open('weather_data.csv', 'w', newline='', encoding='utf-8') as file:
        file.write(response.text)

    print("CSV data has been saved to weather_data.csv")