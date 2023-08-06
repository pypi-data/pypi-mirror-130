"""
Module handles making requests to NewsAPI and then processing
the data recieved from NewsAPI
"""
import json
import requests

def news_API_request(covid_terms="Covid COVID-19 coronavirus")->list:
    """
    Function makes a request to NewsAPI.
    It then processes this data to find articles containing the terms
    given.
    It returns a list of dictionaries. Each dictionary is an article
    """
    with open('config.json',encoding="utf-8") as file:
        config_data=json.load(file)

        api_key=config_data['APIKey']

    lowered_covid_terms=covid_terms.lower()
    term_list=lowered_covid_terms.split()
    #Requests top headlines from the UK from NewsAPI
    url =('https://newsapi.org/v2/top-headlines?'
        'country=gb&'
        'apiKey='+api_key)

    response = requests.get(url)

    news=response.json()['articles']

    covid_articles=[]

    #Iterates through the articles received and finds
    #those which contain the key terms
    for article in news:
        if any(x in article['title'].lower() for x in term_list):
            covid_articles.append(article)

        elif article['description'] is not None:
            if any(x in article['description'].lower() for x in term_list):
                covid_articles.append(article)

    return covid_articles

def update_news(news_to_add:list,removed_news=[])->list:
    """
    Function takes a list of dictionaries as is returned by
    news_API_request. These articles are then checked against
    a list of previously removed articles and any that match
    are removed. Also if there are too many articles some are
    removed.
    A list of dictionaries is returned.
    """
    if isinstance(news_to_add,list):
        #Compares new API response against previously deleted news
        removed_news_title=[]
        for news in removed_news:
            removed_news_title.append(news['title'])

        for article in news_to_add:
            if article['content'] is None or article['title'] in removed_news_title:
                news_to_add.remove(article)

        #Removes article in length is 4 or less
        while len(news_to_add)>4:
            del news_to_add[-1]

        return news_to_add

    return None
