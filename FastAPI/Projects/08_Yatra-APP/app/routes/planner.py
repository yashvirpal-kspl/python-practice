import asyncio

from fastapi import APIRouter,HTTPException
from model import TravelRequestModel
from services.weather import fetch_weather
from services.places import fetch_places
from services.currency import fetch_currency_rates


router = APIRouter(
    prefix="/plan",
    tags=["Travel Plan"]
)

@router.post("/")
async def create_travel_plan(travel_request:TravelRequestModel):
    """
    Aggregate Weather,Currency and Places, into a single travel plan
    """
    if travel_request.start_date > travel_request.end_date:
        raise HTTPException(status_code=400,detail="Start date can not be after end date")
    
    trip_days = (travel_request.end_date-travel_request.start_date).days
    
    if trip_days < 1:
        raise HTTPException(status_code=400,detail="Trip duration must be at least 1 day")
    
    if trip_days > 14:
        raise HTTPException(status_code=400,detail="Trip duration can not exceed 14 days")    

    # Here you would typically call the services to aggregate the travel data (Weather ,Place, Currency)
    weather_data, places_data, currency_data = await asyncio.gather(
        fetch_weather(
            destination=travel_request.destination,
            start_date=travel_request.start_date,
            end_date=travel_request.end_date,
        ),
        fetch_places(travel_request.destination),
        fetch_currency_rates(travel_request.base_currency)
    ) 
    # weather_data = await fetch_weather(
    #     destination=travel_request.destination,
    #     start_date=travel_request.start_date,
    #     end_date=travel_request.end_date,
    # )
    
    # places_data = await fetch_places(travel_request.destination)
    # currency_data = await fetch_currency_rates(travel_request.base_currency)
    
    return {
        "message":"Travel plan create successfully",
        "weather_data":weather_data,
        "places_data":places_data,
        "currency_data":currency_data
    }