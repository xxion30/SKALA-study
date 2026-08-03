"""
프로그램명 : 실무형 수집·검증·품질 파이프라인
과목 : 데이터 분석을 위한 Python 이해
실습 : 종합 실습 1

작성자 : 양시온
작성일 : 2026-08-03

파일 설명
- 검증된 데이터를 DataFrame으로 변환한다.
- CSV와 Parquet 형식으로 저장하고 읽기 및 쓰기 성능을 측정한다.
"""

import time

import pandas as pd


# 데이터를 DataFrame으로 변환하는 함수(Pyantic 모델은 바로 csv로 변환이 어려움)
def create_dataframe(weather, country, ip):

    df = pd.DataFrame({
        "time": weather.time,
        "temperature": weather.temperature_2m,
        "precipitation_probability": weather.precipitation_probability,
    })

    # Weather 정보
    df["latitude"] = weather.latitude
    df["longitude"] = weather.longitude

    # Country 정보
    df["country_name"] = country.name
    df["capital"] = country.capital
    df["population"] = country.population

    # IP 정보
    df["ip_country"] = ip.country
    df["ip_city"] = ip.city

    return df

# 데이터를 CSV 파일로 저장하는 함수
def save_csv(df):
    start = time.perf_counter()

    df.to_csv("output/weather_data.csv", index=False)

    end = time.perf_counter()

    return end - start

# 데이터를 Parquet 파일로 저장하는 함수
def save_parquet(df):
    start = time.perf_counter()

    df.to_parquet("output/weather_data.parquet", index=False)

    end = time.perf_counter()

    return end - start

# 읽기 속도 측정
# csv 파일 읽기 속도 측정
def read_csv():
    start = time.perf_counter()

    pd.read_csv("output/weather_data.csv")

    end = time.perf_counter()

    return end - start

# Parquet 파일 읽기 속도 측정
def read_parquet():
    start = time.perf_counter()

    pd.read_parquet("output/weather_data.parquet")

    end = time.perf_counter()

    return end - start

