from selectolax.lexbor import LexborHTMLParser
import httpx

from .model import (
    WeathersResult,
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
import random
import csv

headers = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
        "(KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36 OPR/102.0.0.0 "
        "(Edition GX-CN)"
    )
}
def search_news(query:str) -> dict:
    """search news from yahoo.

    Args:
        query(str):the search content
    
    example:

        import yahoo_search
        from yahoo_search import search_news

        result=search_news("taiwen)
        print(result.result[0])

        >>>SearchNews(
            source="https://tw.news.yahoo.com/(...)"
            title=""
            context=""
            thumbnail:"https://s.yimg.com/(...)"
        )

    returns: 
        result=[SearchNews()...]

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

    returns:
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
            quote_plus(city+"-city"),
            quote_plus(town+"-city"),
            WOEID
            )
        )

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



def weather():
    ...