from pydantic import BaseModel
from datetime import datetime

class BaseAir(BaseModel):
    pm1: int
    pm25: int
    pm10: int
    temperature: float
    humidity: float
    TVOC: float
    CH2O: float
    CO2: int


class AirCreate(BaseAir):
    pass

class AirRead(BaseAir):
    datetime: str
    pass
