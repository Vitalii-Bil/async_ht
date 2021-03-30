import asyncio
import requests
import os

async def main():
    '''This application collect current London temp from 3 API services and then compare them.'''
    openweathermap_api_key = os.environ.get("openweathermap_api_key")
    weatherbit_api_key = os.environ.get("weatherbit_api_key")

    url1 = 'https://www.metaweather.com/api/location/44418/'
    url2 = f'http://api.openweathermap.org/data/2.5/weather?q=London,uk&APPID={openweathermap_api_key}'
    url3 = f'https://api.weatherbit.io/v2.0/current?lat=51.509865&lon=-0.118092&key={weatherbit_api_key}&include=minutely'

    loop = asyncio.get_event_loop()
    future1 = loop.run_in_executor(None, requests.get, url1)
    future2 = loop.run_in_executor(None, requests.get, url2)
    future3 = loop.run_in_executor(None, requests.get, url3)
    response1 = await future1
    response2 = await future2
    response3 = await future3
    temp1 = float(response1.json()['consolidated_weather'][0]['the_temp'])
    temp2 = float(response2.json()['main']['temp'])
    temp3 = float(response3.json()['data'][1]['temp'])
    av_temp = (temp1 + temp2 + temp3) / 3

    print(f'Temp in London = {av_temp}')

loop = asyncio.get_event_loop()
loop.run_until_complete(main())
