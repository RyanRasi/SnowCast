from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

import request, snowcast

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
            "yearly_forecast": yearly_forecast

        }
        
        return JSONResponse(content=data)
    else:
        return "One or more query params are empty"