import pytest
from pydantic import ValidationError

from models import CountryModel, IpModel, WeatherModel


# WeatherModel 정상 데이터 테스트
def test_weather_model_valid():
    weather = WeatherModel(
        latitude=37.5,
        longitude=127.0,
        time=["2026-08-03T00:00"],
        temperature_2m=[25.3],
        precipitation_probability=[0],
    )

    assert weather.latitude == 37.5
    assert weather.longitude == 127.0


# WeatherModel 잘못된 데이터 테스트
def test_weather_model_invalid():
    with pytest.raises(ValidationError):
        WeatherModel(
            latitude="서울",      # float가 아니라 문자열
            longitude=127.0,
            time=["2026-08-03T00:00"],
            temperature_2m=[25.3],
            precipitation_probability=[0],
        )


# CountryModel 테스트
def test_country_model():
    country = CountryModel(
        name="Korea (Republic of)",
        capital="Seoul",
        population=51780579,
        region="Asia",
        area=100210,
    )

    assert country.capital == "Seoul"
    assert country.population == 51780579


# IpModel 테스트
def test_ip_model():
    ip = IpModel(
        country="United States",
        city="Ashburn",
        lat=39.03,
        lon=-77.50,
    )

    assert ip.country == "United States"
    assert ip.city == "Ashburn"