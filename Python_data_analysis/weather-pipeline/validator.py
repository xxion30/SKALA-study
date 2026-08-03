
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