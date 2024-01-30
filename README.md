# SnowCast
A Machine Learning LSTM weather forecasting tool designed to predict snowfall patterns and identify optimal snow seasons for various destinations. Leveraging machine learning and historical weather data, SnowCast offers insights into the timing, intensity, and duration of snowfall, helping travelers plan their winter activities more effectively.

## Key Features

- **Snowfall Prediction:** Accurately forecasts snowfall amounts and patterns over specified time frames.
- **Seasonal Insights:** Identifies peak snow seasons based on historical data and weather trends.
- **Destination-specific Forecasts:** Provides location-specific snowfall forecasts for selected destinations.
- **User-friendly Interface:** Intuitive and interactive interface for easy exploration of snow-related predictions.

## Technologies Used

- Python
- Machine Learning (TensorFlow)
- Weather APIs (VisualCrossing)
- Data Visualization (Matplotlib, Pandas)

## Getting Started

### Pre-requisites
1. Clone the repository:
```
git clone https://github.com/ryanrasi/SnowCast.git
```
2. Go to visualcrossing, create an account and within the ./microservices/lstm_api folder, create a file called .env
3. Within this file type API_KEY= and paste your API key e.g.
```
API_KEY = "XXXXXXXXXXXXXXXXXXXXXXXXX"
```

### Docker Container

1. Run ```docker-compose build```
2. Run ```docker-compose up```

### Local Hosting

1. Open two terminals and cd into the repo within the folder directory
2. In terminal A, cd into the snowcast folder ```cd snowcast```
3. In terminal B, cd into the microservices/lstm_api folder ```cd microservices/lstm_api```
4. In both terminals run ```pip install -r requirements.txt```
5. In terminal A, run ```python manage.py collectstatic```, ```python manage.py makemigrations```, ```python manage.py migrate```, ```python manage.py runserver```, and accept the 'yes' prompts
6. In terminal B, ```run uvicorn main:app --host 0.0.0.0 --port 8001```

### How to use

1. Open your browser to either your localhost(if you built locally) or your docker IP followed by the port 8000. E.g. ```localhost:8000```
2. Type in a location as well as the duration you wish to predict the optimal snow conditions for.
3. Your results will be visible upon clicking on 'Predict'.

### Methodology

The training data was provided by VisualCrossing in a 365 day period from the current date. This is to provide accurate predictions at the consequence of conducting the training after the user has clicked predict.