from pydantic import BaseModel
from typing import Dict,Optional,List

class WeatherForecast(BaseModel):
    day:str
    weather_img_url:str
    rainfall_img:str
    rainfall_chance:str
    highest_temperature:str
    lowest_temperature:str

class WeatherInformtion(BaseModel):
    locate:str
    city:str
    now:str
    status:str
    temperature_Celsius:str
    temperature_Fahrenheit:str
    highest_temperature:str
    lowest_temperature:str

class Weather(BaseModel):
    result:Dict[WeatherForecast]

class SearchNews(BaseModel):
    source:str
    title:Optional[str]=None
    context:Optional[str]=None
    thumbnail:Optional[str]=None

class News(BaseModel):
    result:List[SearchNews]

class Videos(BaseModel):
    link:str
