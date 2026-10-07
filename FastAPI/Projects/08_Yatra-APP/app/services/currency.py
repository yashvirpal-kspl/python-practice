import httpx
from services.cache import get_cache,set_cache,clear_cache

from dotenv import load_dotenv
import os
load_dotenv()

async def fetch_currency_rates(
    base_currency: str
) -> dict[str, float]:
    cache_key = f"currency_{base_currency}"
    cached_data = get_cache(cache_key)
    
    if cached_data:
        return cached_data
    
    currency_api_key = os.getenv("EXCHANGE_RATE_API_KEY")

    if not currency_api_key:
        raise ValueError("EXCHANGE_RATE_API_KEY is not configured")

    url = (
        f"https://v6.exchangerate-api.com/v6/"
        f"{currency_api_key}/latest/{base_currency.upper()}"
    )

    async with httpx.AsyncClient() as client:
        response = await client.get(url)

        response.raise_for_status()

        data = response.json()

        if data.get("result") != "success":
            raise ValueError(
                f"Currency API error: {data.get('error-type', 'unknown error')}"
            )
        
        rates = data.get("conversion_rates",{})
        set_cache(cache_key,rates,ttl=3600)

        return rates