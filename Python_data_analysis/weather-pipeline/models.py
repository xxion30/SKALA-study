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