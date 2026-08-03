"""
프로그램명 : 실무형 수집·검증·품질 파이프라인
과목 : 데이터 분석을 위한 Python 이해
실습 : 종합 실습 1

작성자 : 양시온
작성일 : 2026-08-03

파일 설명
- Open-Meteo, Countries.dev, ip-api의 데이터를 비동기로 수집한다.
- asyncio와 httpx를 사용하여 여러 API를 동시에 호출한다.
"""

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