from sqlmodel import SQLModel, Field


class Air(SQLModel, table=True):
    __tablename__ = "air"

    id: int = Field(
        default=None,  # 自增.前提是等号左侧不可以None 并且 是主键
        primary_key=True
    )

    datetime: str
    pm1: int
    pm25: int
    pm10: int
    temperature: float
    humidity: float
    TVOC: float
    CH2O: float
    CO2: int