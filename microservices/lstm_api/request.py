import requests
import io
from dotenv import dotenv_values

def fetch(location):
    # Load variables from .env file
    env_vars = dotenv_values(".env")

    # Access variables
    API_KEY = env_vars.get("API_KEY")

    API_DAY_RANGE = 365
    API_LOCATION = location
    API_REQUEST = f"https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/{API_LOCATION}/last{API_DAY_RANGE}days?include=days&key={API_KEY}&contentType=csv"
    print(API_REQUEST)

    response = requests.get(API_REQUEST)
                    
    if response.status_code != 200:
        print('Request failed\nStatus code: ', response.status_code)
        exit()
    else:
        data = pd.read_csv(io.StringIO(response.text))
        return data