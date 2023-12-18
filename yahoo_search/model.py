from pydantic import BaseModel
from typing import Dict,Optional,List


class SearchNews(BaseModel):
    source:str
    title:Optional[str]=None
    context:Optional[str]=None
    thumbnail:Optional[str]=None

class News(BaseModel):
    result:List[SearchNews]
    
class WeatherInformtion(BaseModel):
    locate:str
    city:str
    now:str
    status:str
    temperature_Celsius:str
    temperature_Fahrenheit:str
    highest_temperature:str
    lowest_temperature:str

class Videos(BaseModel):
    link:str

class search(BaseModel):
    link:str