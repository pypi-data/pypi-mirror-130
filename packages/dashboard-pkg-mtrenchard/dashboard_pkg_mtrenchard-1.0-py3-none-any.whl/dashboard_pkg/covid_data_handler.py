"""This module handles all functions and procedures
related to dealing with fetching and porcessing covid
data from both csv files and the covid API
"""
import csv
import sched
import time
from datetime import datetime
from uk_covid19 import Cov19API

s=sched.scheduler(time.time, time.sleep)

def parse_csv_data(csv_filename:str)->list:
    """
    Function takes a csv filename and proccesses the data.
    The function returns a list of strings with each string
    being a seperate row from the csv file.
    """

    with open(csv_filename,'r',encoding="utf-8") as file:
        data=csv.reader(file)
        rows = []
        for row in data:
            #Creates a string in which values are seperated by commas
            day=row[0]+","+row[1]+","+row[2]+","+row[3]+","+row[4]+","+row[5]+","+row[6]
            rows.append(day)

    return rows

def process_covid_csv_data(covid_csv_data):
    """
    Function takes csv data in either a list or dictionary form.
    If the data comes in list form then non useful columns are
    removed. If the data is a dictionary then a list is created
    from the dictionary values
    Then the data is extracted and returned as integers
    Note: when calculating last 7 days cases a day is ignored
    if it has less than half the previous day's cases as this
    would be a significant drop in cases suggesting a more likely
    reason is simply incomplete data.
    """
    useful_data=[]
    if isinstance(covid_csv_data,list):
        #Eliminating column headers and columns that don't contain useful data
        for i in range(0,len(covid_csv_data)):
            row=covid_csv_data[i].split(',')
            del row[:4]
            useful_data.append(row)

        del useful_data[:1]

    elif isinstance(covid_csv_data,dict):
        useful_data=list(covid_csv_data.values())

    #Finding Cumulative Deaths
    found=False
    cum_deaths=0
    row=0
    while found is False and row<len(useful_data):
        if useful_data[row][0]=='' or useful_data[row][0] is None:
            row+=1

        else:
            cum_deaths=int(useful_data[row][0])
            found=True

    #Finding Hospital Cases
    found=False
    hospital_cases=0
    row=0
    while found is False and row<len(useful_data):
        if useful_data[row][1]=='' or useful_data[row][1] is None:
            row+=1

        else:
            hospital_cases=int(useful_data[row][1])
            found=True

    #Finding Last 7 Day Cases
    found=False
    last_7_days=0
    row=0
    #While loop will find the first value of valid case data
    while found is False and row<len(useful_data):
        #Will ignore data if reported cases are less than half of previous day
        if useful_data[row][2]=='' or \
           useful_data[row][2] is None or \
           int(useful_data[row][2])<int(useful_data[row+1][2])*0.5:
            row+=1

        else:
            found=True

    #Accumulates 7 days of data starting at the day with first valid data
    for i in range(row,row+7):
        last_7_days=last_7_days+int(useful_data[i][2])

    return last_7_days,hospital_cases,cum_deaths

def covid_API_request(location="Exeter",location_type="ltla")->dict:
    """
    Function sends a request to the UK covid API
    This data recieved is then processed into a dictionary
    with dates as keys and a list of data as values
    """
    #Use UK covid interactive map to easily find location names
    location=['areaType='+location_type,'areaName='+location]

    cases_and_deaths = {
        "Date": "date",
        "CumDeaths": "cumDailyNsoDeathsByDeathDate",
        "HospitalCases": "hospitalCases",
        "NewCases": "newCasesBySpecimenDate",
    }

    api=Cov19API(filters=location, structure=cases_and_deaths)

    data=api.get_json()

    unparsed_dict=data["data"]
    parsed_dict={}

    #Formats data as dictionary with dates as keys.
    #Values are strings formatted the same as the extracted csv data
    for i in range(0,len(unparsed_dict)):
        values=[unparsed_dict[i]["CumDeaths"],\
                unparsed_dict[i]["HospitalCases"],\
                unparsed_dict[i]["NewCases"]]
        parsed_dict[unparsed_dict[i]["Date"]]=values

    return parsed_dict

def schedule_time_calculator(update_interval:str)->int:
    """
    Function recieves a time string in HH:MM form and then returns
    how many seconds until the time is next reached
    """
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    interval=0
    #current_time_sec and update_sec are how many seconds from 00:00 the time is.
    current_time_sec=int(current_time[0:2])*60*60+int(current_time[3:5])*60+int(current_time[6:8])
    update_sec=int(update_interval[0:2])*60*60+int(update_interval[3:5])*60
    #If the delta is positive it means that the scheduled time is for the current day
    #If it's negative it needs to be scheduled tomorrow
    delta=update_sec-current_time_sec

    if delta>0:
        interval=delta

    elif delta<0:
        interval=(24*60*60-current_time_sec)+update_sec

    return interval

def schedule_covid_updates(update_interval,update_name):
    """
    Function recieves a time in seconds and then schedules
    a covid update in n seconds.
    """
    s.enter(update_interval,1,process_covid_csv_data,argument=(covid_API_request("Exeter","ltla"),))
    s.run()
