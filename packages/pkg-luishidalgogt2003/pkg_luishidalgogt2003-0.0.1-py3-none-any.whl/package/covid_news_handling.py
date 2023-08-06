from covid_data_handler import *
import sys

""" This Module imports everything from covid_data_handler module and imports a news API with all the Covid news in the world"""
logger.info("covid_news_handling module:")


def news_API_request(covid_terms=data["covid_terms"]):
    
    """ gets the news from the api in base_url and from the parameter covid_terms, and query it searches through each parameter
    in covid_terms and returning a list of articles"""
    logger.info("news_API_request:({0})".format(covid_terms))
    articles_check = []
    base_url = "https://newsapi.org/v2/everything?q="
    api_url = "&apiKey="
    api_key = data["api_key"]
    try:
        """ testing whether the API tries has reached a limit as there is only 100 tries per 24h """
        logger.debug("Looping through all the articles related to ({0})".format(covid_terms))
        for query in covid_terms.split(" "):    
            complete_url = base_url + query + api_url + api_key
            news_check = requests.get(complete_url).json()
            articles_check += news_check["articles"]
    except KeyError:
        """ stops everything from running """
        sys.exit("No more API tries, try again later.")
    logger.debug("returns the news articles")
    return articles_check


def test_news_API_request():
    assert news_API_request()
    assert news_API_request('Covid COVID-19 coronavirus') == news_API_request()


def update_news(news_name, news_interval):
    """ schedules updates for the data returned from the news_API_request """
    logger.info("schedule_covid_updates:({0}, {1})".format(news_name, news_interval))
    logger.debug("updating News Articles")
    s.enter(news_interval, 1, news_name, "")
    print("updating news articles...")


def test_update_news():
    update_news('test')