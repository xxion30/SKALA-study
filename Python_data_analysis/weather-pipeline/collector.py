import asyncio

import httpx

#url 정의 - wather, country, ip
WEATHER_URL = (
    "https://api.open-meteo.com/v1/forecast"
    "?latitude=37.5665"
    "&longitude=126.9780"
    "&hourly=temperature_2m,precipitation_probability"
    "&forecast_days=3"
    "&timezone=Asia/Seoul"
)

COUNTRY_URL = "https://countries.dev/alpha/KOR"

IP_URL = "http://ip-api.com/json/8.8.8.8"

#하나의 api를 가져오는 함수
async def fetch(url):
    async with httpx.AsyncClient() as client:
        response = await client.get(url)
        response.raise_for_status()
        return response.json()


#3개의 api를 동시에 가져오는 함수
async def collect_all():
    weather, country, ip = await asyncio.gather(
        fetch(WEATHER_URL),
        fetch(COUNTRY_URL),
        fetch(IP_URL),
    )

    return {
        "weather": weather,
        "country": country,
        "ip": ip,
    }