"""
프로그램명 : 실무형 수집·검증·품질 파이프라인
과목 : 데이터 분석을 위한 Python 이해
실습 : 종합 실습 1

작성자 : 양시온
작성일 : 2026-08-03

파일 설명
- Pydantic v2 모델을 정의한다.
- API에서 수집한 데이터의 타입과 구조를 검증한다.
"""

from pydantic import BaseModel


class WeatherModel(BaseModel):
    latitude: float
    longitude: float
    time: list[str]
    temperature_2m: list[float]
    precipitation_probability: list[int]


class CountryModel(BaseModel):
    name: str
    capital: str
    population: int
    region: str
    area: float


class IpModel(BaseModel):
    country: str
    city: str
    lat: float
    lon: float