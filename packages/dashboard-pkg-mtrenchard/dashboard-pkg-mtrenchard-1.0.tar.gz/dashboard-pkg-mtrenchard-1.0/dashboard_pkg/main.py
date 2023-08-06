"""Imports modules from covid_data_handler and covid_news_handling to
to create the user interface using flask to run a development server
which runs the index.html script
"""
import logging
import time
import sched
import json
from flask import Flask
from flask import render_template
from flask import request
from covid_data_handler import covid_API_request
from covid_data_handler import schedule_time_calculator
from covid_data_handler import process_covid_csv_data
from covid_news_handling import news_API_request
from covid_news_handling import update_news

#Flask has inbuilt logger called werkzeug
logging.getLogger('werkzeug').setLevel(logging.INFO)
logging.basicConfig(filename='logging.log', encoding='utf-8',
level=logging.WARNING,format=\
'%(asctime)s - %(module)s - %(funcName)s - %(lineno)s - %(name)s - %(levelname)s - %(message)s')

with open('config.json',encoding="utf-8") as file:
    config_data=json.load(file)

app=Flask(__name__)
s=sched.scheduler(time.time, time.sleep)
location=config_data['location']
nation=config_data['nation']
area_type=config_data['areaType']
national_7_day_infections,national_hospital,national_cum_deaths,local_7_day_infections=0,0,0,0
updates=[]
removed_news=[]

try:
    local_7_day_infections=process_covid_csv_data(covid_API_request(location,area_type))[0]
    national_7_day_infections,national_hospital,national_cum_deaths=\
    process_covid_csv_data(covid_API_request(nation,"nation"))
except Exception as error:
    logging.error(error)

try:
    news_articles=update_news(news_API_request(),removed_news)
except Exception as error:
    logging.error(error)

def update_covid_data(update: dict):
    """Procedure takes in an update as dictionary
    If the update is in the global list updates it calls the
    covid_API_request and process_covid_csv_data functions
    """
    try:
        #Checks update is in the update array meaning if update is deleted it is cancelled
        if update in updates:
            local_7_day_infections=process_covid_csv_data(covid_API_request(location,area_type))[0]
            national_7_day_infections,national_hospital,national_cum_deaths=\
            process_covid_csv_data(covid_API_request(nation,"nation"))
    except Exception as error:
        logging.error(error)

def news_updater(update: dict):
    """Procedure takes in an update as dictionary.
    If the update is in the global list updates it calls the
    news_API_request and update_news functions
    """
    try:
        #Checks update is in the update array meaning if update is deleted it is cancelled
        if update in updates:
            news_articles=update_news(news_API_request(),removed_news)
    except Exception as error:
        logging.error(error)

def update_creator(name: str)->dict:
    """Takes the name of an update to be created as string.
    The function then fetches all the other nessacary update
    information using flask request module.
    Finally creates a dictionary with this information which
    is appended to global list updates. The dictionary update
    is returned
    """
    repeat=request.args.get('repeat')
    update_time=request.args.get('update')
    covid_data=request.args.get('covid-data')
    news=request.args.get('news')

    content=update_time+" - "
    if repeat=='repeat':
        content="Repeats at "+content

    if covid_data=='covid-data' and news=='news':
        content=content+"Update covid data and news articles"

    elif covid_data=='covid-data':
        content=content+"Update covid data "

    elif news=='news':
        content=content+"Update news"

    update={'title':name,
            'content':content,
            'time':update_time,
            'repeat':repeat,
            'covidData':covid_data,
            'news':news
            }

    updates.append(update)

    return update

def update_remover(update: dict):
    """Takes an update to delete as a dictionary.
    Then removes the update from global list updates
    """
    if update in updates:
        updates.remove(update)

def news_remover(title_to_delete: str):
    """Takes the title of an article to delete as a string.
    Then removes the article from global list news_articles"
    """
    for article in news_articles:
        if article['title']==title_to_delete:
            removed_news.append(article)
            news_articles.remove(article)

def update_scheduler(update: dict):
    """Procedure takes the update to be scheduled as a dictionary.
    The values of this dictionary are then checked to see what
    updates need to be scheduled depending on what options have
    been selected. If the update repeats the procedure will call
    itself
    """
    if update in updates:
        interval=schedule_time_calculator(update['time'])

        if update['covidData']=='covid-data':
            s.enter(interval,1,update_covid_data,(update,))

        if update['news']=='news':
            s.enter(interval,1,news_updater,(update,))

        if update['repeat']=='repeat':
#If the update repeats, on completion of one update the update is passed into the scheduler again
            s.enter(interval,1,update_scheduler,(update,))

        else:
            #If the update doesn't repeat it's removed when completed
            s.enter(interval,1,update_remover,(update,))

@app.route('/index')
def hello():
    """Function which acts on the /index path.
    If an input is submitted by the user from the html
    script different functions and procedures are triggered
    to handle this input.
    Function returns a list of information to be rendered
    by html script.
    """
    s.run(blocking=False)
    update_name=request.args.get('two')
    if update_name:
        update_scheduler(update_creator(update_name))
    update_to_delete=request.args.get('update_item')
    if update_to_delete:
        for update in updates:
            if update['title']==update_to_delete:
                update_remover(update)

    news_to_delete=request.args.get('notif')
    if news_to_delete:
        news_remover(news_to_delete)

    return render_template('index.html',
                           location=location,
                           local_7day_infections=local_7_day_infections,
                           nation_location=nation,
                           national_7day_infections=national_7_day_infections,
                           hospital_cases="Hospital cases: "+str(national_hospital),
                           deaths_total="Total deaths: "+str(national_cum_deaths),
                           news_articles=news_articles,
                           updates=updates,
                           image="image.jpg",
                           title='Covid Updates'
                           )


if __name__ == '__main__':
    app.run()
