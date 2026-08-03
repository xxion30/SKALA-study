"""
프로그램명 : 실무형 수집·검증·품질 파이프라인
과목 : 데이터 분석을 위한 Python 이해
실습 : 종합 실습 1

작성자 : 양시온
작성일 : 2026-08-03

파일 설명
- API 응답에서 필요한 데이터를 추출한다.
- Pydantic 모델을 이용하여 데이터 유효성을 검증한다.
"""

from models import CountryModel, IpModel, WeatherModel


def validate_data(data):
    # Weather 데이터 추출
    weather_raw = data["weather"]

    weather_data = {
        "latitude": weather_raw["latitude"],
        "longitude": weather_raw["longitude"],
        "time": weather_raw["hourly"]["time"],
        "temperature_2m": weather_raw["hourly"]["temperature_2m"],
        "precipitation_probability": weather_raw["hourly"]["precipitation_probability"],
    }

    # Country 데이터 추출
    country_raw = data["country"]

    country_data = {
        "name": country_raw["name"],
        "capital": country_raw["capital"],
        "population": country_raw["population"],
        "region": country_raw["region"],
        "area": country_raw["area"],
    }

    # IP 데이터 추출
    ip_raw = data["ip"]

    ip_data = {
        "country": ip_raw["country"],
        "city": ip_raw["city"],
        "lat": ip_raw["lat"],
        "lon": ip_raw["lon"],
    }

    weather = WeatherModel(**weather_data)
    country = CountryModel(**country_data)
    ip = IpModel(**ip_data)

    return weather, country, ip