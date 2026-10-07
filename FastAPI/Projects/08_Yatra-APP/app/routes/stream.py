from fastapi import APIRouter,HTTPException
from model import TravelRequestModel
from services.weather import fetch_weather
from services.places import fetch_places
from services.currency import fetch_currency_rates
from fastapi.responses import StreamingResponse
import json
from datetime import date,datetime
from pydantic import BaseModel


router =APIRouter(
    prefix="/stream",
    tags=["Stream"]
)

def _jsonable(value):
    if isinstance(value, BaseModel):
        return value.model_dump()
    if isinstance (value,(date,datetime)):
        return value.isoformat()
    if isinstance(value, dict):
        return {
            key: _jsonable(val)
            for key, val in value.items()
        }

    if isinstance(value, list):
        return [_jsonable(item) for item in value]

    return value

def format_sse(data:str,event:str =None)-> str:
    json_data = json.dumps(_jsonable(data))
    
    return f"data: {json_data}\n\n" if event is None else f"event: {event}\ndata: {json_data}\n\n"


async def stream_generator(travel_request:TravelRequestModel):
    yield format_sse({"message":"starting travel plan aggregation..."},event="start")
    
    yield format_sse({"message":"fetching weather data..."},event="weather")
    weather_data = await fetch_weather(
        destination=travel_request.destination,
        start_date=travel_request.start_date,
        end_date=travel_request.end_date,
    )
    yield format_sse({"weather_data":weather_data},event="weather_completed")
    
    yield format_sse({"message":"fetching travel options..."},event="options")
    places_data = await fetch_places(destination=travel_request.destination)
    yield format_sse({"places_data":places_data},event="options_completed")
    
    
    
    yield format_sse({"message":"fetching currency data..."},event="currency")
    curreny_data = await fetch_currency_rates(base_currency=travel_request.base_currency)
    yield format_sse({"curreny_data":curreny_data},event="currency_completed")
    
    
    yield format_sse({"message":"Travel plan aggregation completed!"},event="completed")

@router.post("/plan",response_class=StreamingResponse)
async def stream_travel_plan(travel_request:TravelRequestModel):
    """
    Aggregate Weather,Currency and Places, into a single travel plan to stream
    """
    if travel_request.start_date > travel_request.end_date:
        raise HTTPException(status_code=400,detail="Start date can not be after end date")
    
    trip_days = (travel_request.end_date-travel_request.start_date).days
    
    if trip_days < 1:
        raise HTTPException(status_code=400,detail="Trip duration must be at least 1 day")
    
    if trip_days > 14:
        raise HTTPException(status_code=400,detail="Trip duration can not exceed 14 days")  
    
    
    return StreamingResponse(
        stream_generator(travel_request),
        media_type="text/event-stream",
        headers={"Cache-COntrol": "no-cache","Connection":"keep-alive"}
    )