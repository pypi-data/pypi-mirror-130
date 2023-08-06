"""
NEWS HANDLER
=============

Module deals with newsAPI requests, can get news articles
format them, and create a list to display on UI
"""

import json
import logging
import os
from flask import Markup
import requests

#Loads the config data, to be used throughout the module (using abs path)
this_directory = os.path.dirname(__file__)
with open(os.path.join(this_directory, 'config.json'),encoding="utf-8") as f:
    config_data = json.load(f)

def news_API_request(covid_terms:str = config_data['defaultNewsTerms']) -> list:
    """
    Sets up a query using the input terms, query is then inputted into
    newsAPI and articles returned are put into a list

    Args: covid_terms - String, Terms to specify what news articles will
    be retured, API only returns articles that contain one of the terms

    Return: results - List, list of articles containing one of the covid_terms
    """

    results = []

    #Url information used for API request
    complete_url = ""
    news_url = "https://newsapi.org/v2/everything?"
    language = config_data['newsLanguage']
    api_key = config_data['apiKey']

    complete_url = news_url + "language=" + language + "&apiKey=" + api_key
    #Each term is added to the complete url
    term_list = covid_terms.split(' ')
    for term in term_list:

        complete_url = complete_url + "&q=" + term

    results = requests.get(complete_url)
    try:
        results = results.json()["articles"]
        logging.info('NewsAPI request successful!')
    #Critical as program will not run without NewsAPI data being extracted
    except AttributeError:
        logging.error('NewsAPI not returning correct data structure')
        return None
    except KeyError:
        logging.error('API return does not contain "articles" key, API key may be wrong')
        return None

    return results


def update_news(covid_terms:str = config_data['defaultNewsTerms']) -> list:
    """
    Makes a request to the newsAPI, which outputs a list of articles.
    Used to refresh news articles being displayed. Articles are then formatted
    so can be applied to the UI

    Args: covid_terms - String, Terms to specify what news articles will be retured,
    API only returns articles that contain one of the terms

    Return: formatted_updated_articles - List, list of formatted news articles
    """

    #API request is made
    updated_articles = news_API_request(covid_terms)
    try:
        formatted_updated_articles = []

        #Formats and adds headlines to dictionary
        for new_ar in updated_articles:

            url = new_ar['url']
            content_string = Markup('<p>' + new_ar['description'] + '</p>') + Markup('\n')
            #Adds a url link to each news article
            content_string = content_string + Markup('<a href=' + url + '> Read more</a>')

            formatted_article = {
                    "title":new_ar['title'],
                    "content":content_string
                }

            formatted_updated_articles.append(formatted_article)

        return formatted_updated_articles

    except TypeError:
        logging.critical('NewsAPI returning incorrect data type for articles')
        return None


def articles_to_return(current_articles:list, removed_articles:list = []) -> list:
    """
    Perfoms a check on list of articles to see which have been removed,
    and only returns a list of the first 5 non-removed articles

    Args: current_articles - List, list of articles found by news API
    removed_articles - List of articles removed by user on the UI

    Return: to_return - List, Returns 5 articles that haven't yet been
    removed by user
    """

    to_return = []
    try:
        for ar in current_articles:
            try:
                if (ar['title'] not in removed_articles) and (len(to_return) < 5):

                    to_return.append(ar)
            #Checks that article key exists, if this occurs it is not critical
            #as loop checks one article at a time
            except KeyError:
                logging.error('The key "title" does not exist for article')

        return to_return
    #Raised when NewsAPI returns an empty list
    except TypeError:
        logging.error('No articles returned from NewsAPI')
        #If no articles present returns empty list, so html file can still iterate and load webpage
        return []
