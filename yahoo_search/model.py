from pydantic import BaseModel
from typing import Dict,Optional,List


class SearchNews(BaseModel):
    source:str
    title:Optional[str]=None
    context:Optional[str]=None
    thumbnail:Optional[str]=None

class News(BaseModel):
    result:List[SearchNews]
    
class WeathersResult(BaseModel):
    link:str

class Weather(BaseModel):
    ...

class Videos(BaseModel):
    link:str

class search(BaseModel):
    link:str