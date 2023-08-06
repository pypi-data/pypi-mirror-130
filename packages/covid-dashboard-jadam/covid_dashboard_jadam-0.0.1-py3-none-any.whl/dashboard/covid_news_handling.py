'''This module handles importing and sorting data from the news API'''
import logging

from newsapi import NewsApiClient

from covid_data_handler import get_config_data
from covid_data_handler import FORMAT

config = get_config_data('config.json')
logging.basicConfig(format=FORMAT,filename='system.log',level=logging.INFO)

covid_news = []

def news_API_request(covid_terms: str = config['news_keywords']) -> list:
    '''imports news article, and returns them as a dictionary
       arguments: covid_terms: string of words that imported news
                  articles must contain'''

    logging.debug('news_API_request triggered')
    newsapi = NewsApiClient(api_key=config['API_key'])

    covid_news = newsapi.get_everything(q=covid_terms, language='en')

    return covid_news['articles']

def update_news(update_name: str, removed_news: list = []) -> None:
    '''updates the news articles database, while ensuring previously removed
       articles are not returned
       arguments: update_name: the name of the update
                  removed_news: title of previously removed news articles'''

    logging.debug('update_news triggered')
    new_news = news_API_request()

    for new_article in new_news:
        remove = False
        for article in covid_news:
            if new_article == article:
                remove = True

        if len(removed_news) > 0:
            for i in range(0, len(removed_news)):
                if new_article['title'] == removed_news[i]:
                    remove = True

        if remove is True:
            new_news.remove(new_article)

    for new_article in new_news:
        covid_news.append(new_article)

    return covid_news
