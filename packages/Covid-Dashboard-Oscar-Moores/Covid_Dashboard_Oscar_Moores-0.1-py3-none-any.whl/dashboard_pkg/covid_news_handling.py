"""Contains the functions for querying the news API and returning the results in a form that allows them to be added to the dashboard"""
from newsapi import NewsApiClient
from flask import Flask, render_template, url_for, request
import requests, json, logging


#Setting up logging file
logging.basicConfig(filename='event_log.log', level=logging.DEBUG)

#Opens config file and loads into the variable config_data then closes the file
file = open("config.json")
config_data = json.load(file)
file.close()

#Requests news articles from the news API using API key found in config file
newsAPI = NewsApiClient(api_key = config_data["news_api_key"])

#Returns the news articles after requesting them from the API
def news_API_request(covid_terms = config_data["search_terms"]):
    """The function takes the parameter covid_terms, which are by default taken from the config file, it then returns an array of dictionaries containing the articles \n
        :param name: covid_terms \n
        :param type: string \n
        :return: list
        """
    logging.debug("Function news_API_request run with parameters: ",covid_terms)

    all_articles = newsAPI.get_everything(q=covid_terms, language = "en", page_size=20)
    return(all_articles["articles"])

#Returns the news articles in a data structure that allows them to be displayed
#on the covid dashboard
def update_news(covid_news = news_API_request()):
    """Function takes the parameter covid_news, which is by default the function news_API_request.
        The function returns the news articles in a data structure which allows them to be displayed by the dashboard \n
        :param name: covid_news - the result of a news api request \n
        :param type: list \n
        :return: list \n
        """
    logging.debug("Function update_news run with parameters: %s",covid_news)

    #Opens config file and loads into the variable config_data then closes the file
    #Makes sure config_data is up to date so excluded articles can be looked up
    file = open("excluded.json")
    excluded_json = json.load(file)
    file.close()

    #Creates a news data structure
    news = []

    #Puts every news article and their title in an array with each index being a dictionary holding 
    #news articles title and content
    articles_found = 0
    index = 0
    try:
        while articles_found < config_data["articles_displayed"]:
            if not(covid_news[index]["title"] in excluded_json["excluded_article_titles"]):
                news.append({"title":covid_news[index]["title"],"content":covid_news[index]["content"]})
                #Only incriments articles found if an appropriate article has been found
                articles_found += 1
            #Always increments index
            index += 1    
    except IndexError:
        logging.error("IndexError in update_news")
    except RuntimeError:
        logging.error("RuntimeError in update_news")
    #Returns the news data structure
    return(news)
        

