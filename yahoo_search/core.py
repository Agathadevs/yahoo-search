import random
import csv
from selectolax.lexbor import LexborHTMLParser
import httpx

from .model import (
    WeatherInformtion,
    SearchNews,
    search,
    Videos,
    News
)

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

    response=client.get("https://tw.news.yahoo.com/search?p={}&fr=uh3_news_web&fr2=p%3Anews%2Cm%3Asb&.tsrc=uh3_news_web".format(quote_plus(query)),
                      headers=headers  )
    
    response_html=LexborHTMLParser(response.text)

    result=[]
    context={}

    all_element=response_html.body.css("div.StreamContainer ul li")
    
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

def weather_search(nation:str,city:str,town:str) -> dict:

    """search weather from ur location.

    Args:
        :nation(str):your nation
        :city(str):your city name
        :town(str):your town name

    Returns:
        ...
    
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
            )
        )

        response_html=LexborHTMLParser(response.text)
        print(response.url)
        

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
    response=client.get("https://tw.news.yahoo.com/weather/",
                        headers=headers)
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