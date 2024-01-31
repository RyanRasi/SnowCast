from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import pandas as pd
import request, snowcast
from fastapi.responses import JSONResponse
import numpy as np
import matplotlib.pyplot as plt
import io
import base64
from matplotlib.dates import MonthLocator, DateFormatter
from datetime import datetime, timedelta

# Set the Matplotlib backend to 'Agg'
plt.switch_backend('Agg')

def generate_plot(data):

    # Get the current date
    current_date = datetime.now()

    # Generate an array of dates for the next year with daily intervals
    start_date = current_date
    end_date = current_date + timedelta(days=len(data))
    date_array = [start_date + timedelta(days=i) for i in range((end_date - start_date).days)]

    # Format the dates as strings in the 'YYYY-MM-DD' format
    formatted_date_array = [date.strftime('%Y-%m-%d') for date in date_array]

    plt.plot(formatted_date_array, data, label='Predicted Snow')
    plt.legend()
    plt.title('Yearly Forecast')
    plt.xlabel('Date')
    plt.ylabel('Inches of Snow')

    # Group x-axis labels by months
    plt.gca().xaxis.set_major_locator(MonthLocator())
    plt.gca().xaxis.set_major_formatter(DateFormatter("%b"))

    # Rotate the x-axis labels for better readability
    plt.gcf().autofmt_xdate()
    # Save the plot to a BytesIO object
    image_stream = io.BytesIO()
    plt.savefig(image_stream, format='png')
    image_stream.seek(0)

    # Encode the BytesIO object to a base64 string
    image_base64 = base64.b64encode(image_stream.read()).decode('utf-8')

    # Close the plot to avoid potential issues with multiple plots
    plt.close()
    # Return the base64-encoded image in the response
    return {"image_base64": image_base64}

app = FastAPI()

# CORS configuration
origins = [
    "http://localhost",
    "http://localhost:8000",
    "http://127.0.0.1:8000"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/recommend/")
def read_item(location_param: str = None, duration_param: str = None):
    if location_param != None and duration_param != None:
        print("location_param", location_param)
        print("duration_param", duration_param)
        api_request = request.fetch(location_param)
        start_short, end_short, start_long, end_long, inches, yearly_forecast = snowcast.recommend(api_request, duration_param)
    
        data = {
            "start_short": start_short,
            "end_short": end_short,
            "start_long": start_long,
            "end_long": end_long,
            "inches": inches,
            "yearly_forecast": generate_plot(yearly_forecast)

        }
        
        return JSONResponse(content=data)
    else:
        return "One or more query params are empty"