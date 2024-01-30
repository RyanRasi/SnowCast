import request, snowcast
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

location_param = 'Hopfgarten'
duration_param = '7'

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
    "yearly_forecast": yearly_forecast

}

print(JSONResponse(content=data))