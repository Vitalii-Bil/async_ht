import asyncio
import requests
import os
from aiohttp import ClientSession

openweathermap_api_key = os.environ.get("openweathermap_api_key")
weatherbit_api_key = os.environ.get("weatherbit_api_key")

url1 = 'https://www.metaweather.com/api/location/44418/'
url2 = f'http://api.openweathermap.org/data/2.5/weather?q=London,uk&APPID={openweathermap_api_key}'
url3 = f'https://api.weatherbit.io/v2.0/current?lat=51.509865&lon=-0.118092&key={weatherbit_api_key}&include=minutely'


async def get_weather(url, session):
    try:
        response = await session.request(method='GET', url=url)
    except requests.exceptions.RequestException as e:
        print ("Error: ", e)
    response = await response.json()
    return response


async def metaweather(url, session):
    response = await get_weather(url, session)
    return float(response['consolidated_weather'][0]['the_temp'])


async def openweathermap(url, session):
    response = await get_weather(url, session)
    return float(response['main']['temp'])


async def weatherbit(url, session):
    response = await get_weather(url, session)
    return float(response['data'][1]['temp'])


async def run_program():
    async with ClientSession() as session:
        result = await asyncio.gather(metaweather(url1, session),
                                      openweathermap(url2, session),
                                      weatherbit(url3, session))
        
        print(f'Temp in London = {(result[0] + result[1] + result[2])/3}')


def main():
    '''This application collect current London temp from 3 API services and then compare them.'''
    loop = asyncio.get_event_loop()
    loop.run_until_complete(run_program())
    loop.close()


if __name__ == "__main__":
    main()
