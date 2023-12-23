import csv
from selectolax.lexbor import LexborHTMLParser
import httpx
from pydantic import BaseModel
from typing import Optional,List

from urllib.parse import (
    quote_plus,
    quote,
    unquote_plus,
    unquote
)

headers = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
        "(KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36 OPR/102.0.0.0 "
        "(Edition GX-CN)"
    )
}

class Search(BaseModel):
    title:str
    url:str
    context:str

class SearchResult(BaseModel):
    result:List[Search]

class SearchNews(BaseModel):
    source:str
    title:Optional[str]=None
    context:Optional[str]=None
    thumbnail:Optional[str]=None

class News(BaseModel):
    result:List[SearchNews]

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

class WeatherSearch(BaseModel):
    locate:str
    city:str
    now:str
    status:str
    temperature_Celsius:str
    temperature_Fahrenheit:str
    highest_temperature:str
    lowest_temperature:str

class Weather(BaseModel):
    result:List[WeatherForecast]

class Videos(BaseModel):
    Videolink:str
    title:Optional[str]=None
    source:Optional[str]=None
    thumbnail:Optional[str]=None
    time:str
    url:str

class VideosResult(BaseModel):
    result:List[Videos]

def search(query:str) -> Search:

    client=httpx.Client()

    content={}
    result=[]

    response=client.get(
        "https://tw.search.yahoo.com/search;_ylt=Awrtg0jwlIFlVr4MMjtr1gt."
        ";_ylu=Y29sbwN0dzEEcG9zAzEEdnRpZAMEc2VjA3BhZ2luYXRpb24-?p={}&fr=s"
        "fp&fr2=sb-top&b=8&pz=7&pstart=3".format(
            quote_plus(query)
        ),
        headers=headers
    )

    response_result=LexborHTMLParser(response.text)
    Search_results=response_result.css_first("h2.title span").text()
    page=response_result.css_first(".reg.searchCenterMiddle")

    for i in page.css("li"):

        if i.attributes:

            continue

        else:
            
            title=i.css_first("h3.title a").text(False)
            url=i.css_first("h3.title span").text()
            context=i.css_first("div.compText p span").text()

            content={
                "title":title,
                "url":url,
                "context":context
            }

            result.append(content)

    return SearchResult(result=result)

def search_news(query:str) -> SearchNews:

    """search news from yahoo.

    Args:
        query(str):the search content
    
    example:
        .. code-block :: python

            import yahoo_search
            from yahoo_search import search_news

            result=search_news("taiwen)
            print(result.result[0])

            >>> SearchNews(
                source="https://tw.news.yahoo.com/(...)"
                title=""
                context=""
                thumbnail:"https://s.yimg.com/(...)"
            )

    Returns: 
        SearchNews:result of search news.

    """            
    client=httpx.Client()

    response=client.get(
        "https://tw.news.yahoo.com/search?p={}&fr=uh3_news_web&fr2=p%3Anews%2Cm%3Asb&.tsrc=uh3_news_web".format(
            quote_plus(
                query
                )
            ),
            headers=headers  
        )
    
    response_html=LexborHTMLParser(response.text)

    result=[]
    context={}
    
    for i in response_html.body.css("div.StreamContainer ul li"):
        
        source_="https://tw.news.yahoo.com{}".format(
            unquote_plus(
                unquote(
                    i.css("h3 a")[0].attributes["href"]
                )
            )
        )

        title_=i.css("h3 a")[0].text()
        context_=i.css("p")[0].text()
        thumbnail_=i.css("img")[0].attributes["src"]

        new_context={
                "source":source_,
                "title":title_,
                "context":context_,
                "thumbnail":thumbnail_
            }
            
        context.update(**new_context)
        result.append(context)

    return News(result=result)

def weather_search(nation:str,city:str,town:str) -> WeatherSearch:

    """search weather from ur location.

    Args:
        :nation(str):your nation
        :city(str):your city name
        :town(str):your town name

    Returns:
        WeatherSearch
    
    """
    locate=[]
    weather={}

    csv_file=open('woeid.csv', 'r',encoding="utf-8")
    data = csv.DictReader(csv_file)  

    for location in data:
        locate.append(location["name"])
        if town in locate :
            WOEID=location["woeid"]

    if nation=="taiwan":

        client=httpx.Client(
        )
        response=client.get(
            "https://tw.news.yahoo.com/weather/"
            "{}/{}/{}-{}".format(
            quote_plus(nation),
            quote_plus(city.replace(city[0],city[0].lower())+"-city"),
            quote_plus(town.replace(city[0],city[0].lower())+"-city"),
            WOEID
            ),
            headers=headers
        )

        response_html=LexborHTMLParser(response.text)

        now=response_html.css_first("div time").text()  
        city=response_html.css_first("div.M\(10px\) h1").text()
        nation=response_html.css_first("div.D\(f\) h2").text()
        temperature_celsius=response_html.css_first("div.temperature-forecast span.Va\(t\).D\(n\)").text()
        temperature_fahrenheit=response_html.css_first("div.temperature-forecast span.Va\(t\).D\(b\)").text()
        weather_status=response_html.css_first("div.My\(2px\).Px\(2px\).D\(f\).Ai\(c\) p").text()
        highest_temperature=response_html.css("div.My\(2px\) span.D\(n\)")[0].text()
        lowest_temperature=response_html.css("div.My\(2px\) span.D\(n\)")[1].text()

        Meteorological_information={
            "locate":f"{nation}",
            "city":city,
            "now":now,
            "temperature_Celsius":str(temperature_celsius)+"°C",
            "temperature_Fahrenheit":str(temperature_fahrenheit)+"°F",
            "status":weather_status,
            "highest_temperature":str(highest_temperature),
            "lowest_temperature":str(lowest_temperature)  
        }

        return WeatherSearch(**Meteorological_information)
        
    else:

        client=httpx.Client(
        )
        response=client.get(
            "https://tw.news.yahoo.com/weather/"
            "{}/{}/{}-{}".format(
            quote_plus(nation),
            quote_plus(city),
            quote_plus(town),
            WOEID
            )
        )
        now=response_html.css_first("div time").text()  
        city=response_html.css_first("div.M\(10px\) h1").text()
        nation=response_html.css_first("div.D\(f\) h2").text()
        temperature_celsius=response_html.css_first("div.temperature-forecast span.Va\(t\).D\(n\)").text()
        temperature_fahrenheit=response_html.css_first("div.temperature-forecast span.Va\(t\).D\(b\)").text()
        weather_status=response_html.css_first("div.My\(2px\).Px\(2px\).D\(f\).Ai\(c\) p").text()
        highest_temperature=response_html.css("div.My\(2px\) span.D\(n\)")[0].text()
        lowest_temperature=response_html.css("div.My\(2px\) span.D\(n\)")[1].text()

        Meteorological_information={
            "locate":f"{nation}",
            "city":city,
            "now":now,
            "temperature_Celsius":str(temperature_celsius)+"°C",
            "temperature_Fahrenheit":str(temperature_fahrenheit)+"°F",
            "status":weather_status,
            "highest_temperature":str(highest_temperature),
            "lowest_temperature":str(lowest_temperature)  
        }

        return WeatherSearch(**Meteorological_information)

def weather() -> WeatherInformtion:

    """serach weather from yahoo.

    example:
        .. code-block :: python

            import yahoo_search
            print(yahoo_search.weather()) 

            >>> WeatherInformation( 
                locate='台灣' ,
                city='臺北市' ,
                time='12/18 下午4:00' ,
                status='陰' ,
                temperature_Celsius='23°C' ,
                temperature_Fahrenheit='73°F' ,
                highest_temperature='24°' ,
                lowest_temperature='17°'
            )

            print(yahoo_search.weather().city)

            >>> "台北市"

        Returns:
            WeatherInformation: ther information of weather.
    """
    client=httpx.Client()

    response=client.get(
        "https://tw.news.yahoo.com/weather/",
        headers=headers
    )

    response_html=LexborHTMLParser(response.text)

    now=response_html.css_first("div time").text()  
    city=response_html.css_first("div.M\(10px\) h1").text()
    nation=response_html.css_first("div.D\(f\) h2").text()
    temperature_celsius=response_html.css_first("div.temperature-forecast span.Va\(t\).D\(n\)").text()
    temperature_fahrenheit=response_html.css_first("div.temperature-forecast span.Va\(t\).D\(b\)").text()
    weather_status=response_html.css_first("div.My\(2px\).Px\(2px\).D\(f\).Ai\(c\) p").text()
    highest_temperature=response_html.css("div.My\(2px\) span.D\(n\)")[0].text()
    lowest_temperature=response_html.css("div.My\(2px\) span.D\(n\)")[1].text()

    Meteorological_information={
        "locate":f"{nation}",
        "city":city,
        "now":now,
        "temperature_Celsius":str(temperature_celsius)+"°C",
        "temperature_Fahrenheit":str(temperature_fahrenheit)+"°F",
        "status":weather_status,
        "highest_temperature":str(highest_temperature),
        "lowest_temperature":str(lowest_temperature)  
    }
    
    return WeatherInformtion(**Meteorological_information)   

def weather_forecast() -> WeatherForecast:

    """search weather forecast from yahoo.

    example:
        .. code-block :: python

            import yahoo_search
            print(core.weather_forecast().result.[0])
            >>> WeatherSearch(
                    day='星期一',
                    weather_img_url='https://s.yimg.com/os/weather/1.0.1/shadow_icon/60x60/rain_day_night@2x.png',
                    rainfall_img='https://s.yimg.com/os/weather/1.0.1/precipitation/54x60/rain_ico_60@2x.png',
                    rainfall_chance='66%',
                    highest_temperature='23°C',
                    lowest_temperature='17°C'
                ) 
    Returns:
        WeatherSearch:weather Forecast from yahoo weather
    """
    client=httpx.Client()

    response=client.get(
        "https://tw.news.yahoo.com/weather/",
        headers=headers
    )

    response_html=LexborHTMLParser(response.text)

    text_=response_html.css_first("div.Miw\(0\) table")

    result=[]
  
    for i in text_.css("tbody tr.Bdb"):
        
        all_=i.css("td")

        day=all_[0].text()[10:13]

        weather_img_url=all_[1].css_first("img").attributes["data-wf-src"]
   
        rainfall_img=all_[2].css_first("img").attributes["data-wf-src"]

        rainfall_chance=all_[2].css_first("dl dd").text()

        highest_temperature=str(all_[3].css_first("dl dd.D\(n\)").text())+"C"

        lowest_temperature=str(all_[3].css_first("dl dd.Pstart\(10px\).celsius_D\(b\)").text())+"C"

        if (
            day,
            weather_img_url,
            rainfall_img,
            rainfall_chance,
            highest_temperature,
            lowest_temperature
        ):
            forecast={
                "day":day,
                "weather_img_url": weather_img_url,
                "rainfall_img":rainfall_img,
                "rainfall_chance":rainfall_chance,
                "highest_temperature":highest_temperature,
                "lowest_temperature":lowest_temperature
            }

        result.append(forecast)

    return Weather(result=result)

def video_search(query:str) -> Videos:

    """search videos from yahoo.
    Args:
        :query(str): query

    Returns:
        Videos
    
    """
    client=httpx.Client()

    response=client.get(
        "https://video.search.yahoo.com/search/video;_ylt="
        "Awr9zCWyaYZlgAUjsSJXNyoA;_ylu=Y29sbwNncTEEcG9zAzE"
        "EdnRpZAMEc2VjA3BpdnM-?p={}&fr2=piv-web&fr=sfp".format(
            quote_plus(
                query
            )
        ),
        headers=headers
    )

    response_html=LexborHTMLParser(response.text)

    text_=response_html.css("div.results.clearfix ol li")

    content={}
    result=[]

    for i in text_:

        thumbnail=i.css_first("div.vthm.fill img").attributes["src"]
        time=i.css_first("div.v-meta.bx-bb div.v-age").text()
        title=i.css_first("div.v-meta.bx-bb h3").text()
        video_link=i.css_first("div.pos-bx.res").attributes["data-movie"]
        source=i.css_first("div.v-meta.bx-bb cite").text()
        url="https://tw.video.search.yahoo.com"+i.css_first("a").attributes["href"]

        content={
            "thumbnail":thumbnail,
            "time":time,
            "title":title,
            "Videolink":video_link,
            "source":source,
            "url":url
        }

        result.append(content)

    return VideosResult(result=result)