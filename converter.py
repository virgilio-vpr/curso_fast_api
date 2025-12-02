from os import getenv
from fastapi import HTTPException
import aiohttp
import requests

ALPHAVANTAGE_API_KEY = getenv("ALPHAVANTAGE_API_KEY")

def sync_converter(from_currency:str, to_currency:str, price:float):
    url= f'https://www.alphavantage.co/query?function=CURRENCY_EXCHANGE_RATE&from_currency={from_currency}&to_currency={to_currency}&apikey={ALPHAVANTAGE_API_KEY}'

    try:
        response = requests.get(url)
    except Exception as error:
        raise HTTPException(status_code=400, detail=error)
    
    data = response.json()

    if "Realtime Currency Exchange Rate" not in data:
        raise HTTPException(status_code=400, detail=f"Realtime Currency Exchange Rate not in response {data}")

    exchange_rate = float(data["Realtime Currency Exchange Rate"]["5. Exchange Rate"])

    return price * exchange_rate


async def async_converter(from_currency:str, to_currency:str, price:float):
    url= f'https://www.alphavantage.co/query?function=CURRENCY_EXCHANGE_RATE&from_currency={from_currency}&to_currency={to_currency}&apikey={ALPHAVANTAGE_API_KEY}'

    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                data = await response.json()

    except Exception as error:
            raise HTTPException(status_code=500, detail=f'Internal error on alpha vantange requests: {error}')

    if "Realtime Currency Exchange Rate" not in data:
            raise HTTPException(status_code=400, detail=f'Probably invalid currencies given {data}') 

 
    exchange_rate = float(data["Realtime Currency Exchange Rate"]["5. Exchange Rate"])
  
    return {to_currency: price * exchange_rate}