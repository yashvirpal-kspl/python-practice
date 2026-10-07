from datetime import date
from model import WeatherResponseModel
import httpx
from services.cache import get_cache,set_cache,clear_cache

from dotenv import load_dotenv
import os
load_dotenv()

async def fetch_weather(
    destination:str,
    start_date:date,
    end_date:date
)->list[WeatherResponseModel]:
    
    cache_key = f"{destination}_{start_date}_{end_date}"
    cached_data = get_cache(cache_key)
    
    if cached_data:
        return cached_data
    weather_api_key = os.getenv("WEATHERAPI_API_KEY")
    
    if not weather_api_key:
        raise ValueError("WEATHERAPI_API_KEY is not configured")


    async with httpx.AsyncClient() as client:
        response = await client.get(
            f"https://api.weatherapi.com/v1/forecast.json",
            params={
                "key":weather_api_key,
                "q":destination,
                "dt":start_date,
                "end_dt":end_date
            }
        )
        
        response.raise_for_status()
        data = response.json()
        
        forecasts = []
        
        for day in data['forecast']['forecastday']:
            forecast = WeatherResponseModel(
                date =day['date'],
                condition =day['day']['condition']['text'],
                temperature_high =day['day']['maxtemp_c'],
                temperature_low =day['day']['mintemp_c'],
                humidity =day['day']['avghumidity'],
                rain_chance =day['day']['daily_chance_of_rain'],
            )
            forecasts.append(forecast)
        set_cache(cache_key,forecasts,ttl=3600) # cache for 1 hour
        return forecasts    
        