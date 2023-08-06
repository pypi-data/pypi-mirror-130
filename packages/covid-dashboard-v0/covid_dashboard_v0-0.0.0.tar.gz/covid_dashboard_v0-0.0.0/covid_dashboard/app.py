"""
DASHBOARD AND SCHEDULE MANAGEMENT
==================================

Module uses flask to display Covid-19 data and news articles to the user.
Module also deals with Update scheduling, provides functions to
schedule new updates and remove them.
"""

import sched
import time
import datetime
import json
import logging
import os
from flask import Flask, render_template, request, Markup
from covid_news_handling import update_news, articles_to_return
from covid_data_handler import formatted_all_data

#Configures Log file
logging.basicConfig(filename='myapp.log', format='%(levelname)s:%(asctime)s %(message)s',
datefmt='%m/%d/%Y %I:%M:%S %p', level=logging.INFO)

#Initialises flask and scheduler
app=Flask(__name__)
scheduler = sched.scheduler(time.time, time.sleep)

#Global variables for storing info for dashboard
display_update = []
removed_articles = []
current_articles = []
current_data = []

#Loads the config data, to be used throughout the module (using abs path)
this_directory = os.path.dirname(__file__)
with open(os.path.join(this_directory, 'config.json'),encoding="utf-8") as f:
    config_data = json.load(f)

#----------------UPDATE SCHEDULING

def schedule_covid_updates(update_interval:str, update_name) -> None:
    """
    Function schedules new update, using sched module, this is then stored in a list
    so can be canceled later on if needed

    Args: update_interval - String, specifies the time the update should go off
    update_name - The function which will be run once update_interval time has been reached
    """

    #As function is called right after new update added to list, can assume update will be
    #at the back of list
    new_update_index = len(display_update) - 1

    new_sched = scheduler.enter(update_interval, 1, update_name,
    (display_update[new_update_index],))
    #Sched is stored with its associated update
    display_update[new_update_index]['scheduler'] = new_sched

    logging.info('New update created: %s', str(display_update[new_update_index]['scheduler']))

def unschedule_update(update_to_remove:dict, remove_from_queue:bool = False) -> None:
    """
    Removes update from the scheduler and the UI

    Args: update_to_remove - Dictionary, dictionary of the Update which should be removed from the
    queue and UI
    remove_from_queue - Boolean, only unschedules update in scheduler if true, used when user
    presses cross button on toast in UI
    """

    if update_to_remove in display_update:
        #Removes update from list displayed on dashboard
        display_update.remove(update_to_remove)

        logging.info('Update deleted from dashboard: %s', str(update_to_remove))
        #Unschedules update if true
        if remove_from_queue:
            try:
                scheduler.cancel(update_to_remove['scheduler'])
                logging.info('Update removed from scheduling queue')
            #Only a warning level as program may continue running without update being canceled
            except ValueError:
                logging.warning('Attemted to unschedule update but update not in sched queue')


def time_difference(update_interval:str) -> float:
    """
    Finds the difference between now and the time input by user

    Args: update_interval - Analogue string, time of when the user wants the update to occur

    Return: difference - Float, The datetime difference between now and the input time
    """

    try:
        #Splits string and converts to int
        split_time = update_interval.split(':')

        split_time[0] = int(split_time[0])
        split_time[1]= int(split_time[1])

        now = datetime.datetime.now()

        #Check performed to see if update time is for today or tomorrow
        if split_time[0] < now.hour:
            update_time = now + datetime.timedelta(days=1)
        elif split_time[0] == now.hour and split_time[1] < now.minute:
            update_time = now + datetime.timedelta(days=1)
        elif split_time[0] == now.hour and split_time[1] == now.minute:
            update_time = now + datetime.timedelta(days=1)
        else:
            update_time = now

        #Placed into datetime format and the difference is found
        update_time = datetime.datetime(update_time.year,update_time.month,update_time.day,
        split_time[0],split_time[1],0)

        difference = update_time - now
        difference = difference.total_seconds()

        return difference
    #Set to an error, as although inputted time is incorrect, program can stil continue
    except ValueError:
        logging.error('User input time is not in correct format. (Input was: %s )',
        str(update_interval))
        return 0
    except IndexError:
        logging.error('User input time is not in correct format. (Input was: %s )',
        str(update_interval))
        return 0

def function_to_schedule(update_time:str, repeat:bool, covid_data:bool, news:bool) -> None:
    """
    Determines which function needs to be updated once scheduler has reached end of
    update interval

    Args: update_time - str, time of update
    repeat - bool, will it repeat?
    covid_data - bool, update covid data?
    news - bool, update news articles?
    """

    #Finds the interval between now and update time
    difference = time_difference(update_time)
    #Chooses which parts of page need updating on schedule
    if repeat:
        schedule_covid_updates(difference, recursive_update)
    else:
        if covid_data and news:
            schedule_covid_updates(difference, update_both)
        elif covid_data:
            schedule_covid_updates(difference, update_covid_data)
        elif news:
            schedule_covid_updates(difference, update_current_articles)
        else:
            schedule_covid_updates(difference, unschedule_update)

#---------------APP

@app.route('/')
def home():
    """
    Runs when UI first opened, updates covid-19 data and news articles
    """

    #Updates covid and news data when UI launched
    update_both('')
    #Runs update_schedule to render UI
    return update_schedule()


@app.route('/index', methods = ['POST', 'GET'])
def update_schedule() -> render_template:
    """
    Deals with removing toasts, creating and scheduling new updates
    and rendering html template, function ran every 60 seconds
    """

    #Scheduler queue checked every time function runs (every 60 seconds)
    scheduler.run(blocking=False)
    #From config file location and nation are gotten and formatted for display
    try:
        user_location = Markup('<b>' + config_data['location'] + '</b>')
        user_nation = Markup('<b>' + config_data['nation'] + '</b>')
    #Critical as program cannot work without user location
    except KeyError:
        logging.critical('"location" or "nation" key not found in config file')

    if request.method == 'GET':
        #Checks if user has clicked cross on any toast widgets
        update_to_remove = request.args.get('update_item')
        article_to_remove = request.args.get('notif')
        #Update removal
        if update_to_remove:
            for update in display_update:
                try:
                    if update['title'] == update_to_remove:
                        unschedule_update(update, True)
                #Only warning as program can continue without removing update
                except KeyError:
                    logging.warning('Attempted to remove update but key "title" does not exist')

        #Article removal
        if article_to_remove:
            #Adds to list of removed articles
            removed_articles.append(article_to_remove)
            #Displays removed article in log file
            logging.info('Article removed: %s', str(article_to_remove))

        name = request.args.get('two')
        #Checks if user has entered an update
        if name:
            #If so rest of form is gotten
            update_time = request.args.get('update')
            repeat = bool(request.args.get('repeat'))
            covid_data = bool(request.args.get('covid-data'))
            news = bool(request.args.get('news'))
            #Checks there are no updates already with the same name
            duplicate = False
            for update in display_update:
                if update['title'] == name:
                    logging.error('Update name [%s] already being used for other update', name)
                    duplicate = True

            if not duplicate:
                #Toast is built and displayed to user
                toast_builder(name,update_time,repeat,covid_data,news)
                function_to_schedule(update_time,repeat,covid_data,news)

        #Every refresh of the webpage, checks that there are 5 articles displayed to user
        #DOESNT refresh articles, just accesses an already gotten list
        articles_to_output = articles_to_return(current_articles, removed_articles)

    return render_template('index.html', title = Markup('<b>COVID-19 Statistics</b>'),
                        location=user_location, local_7day_infections=current_data[0],
                        nation_location=user_nation, national_7day_infections = current_data[1],
                        hospital_cases = current_data[2], deaths_total = current_data[3],
                        updates=display_update, news_articles=articles_to_output,
                        image='image.jpeg',favicon='image.jpeg')

def toast_builder(update_name:str,update_time:str,repeat:bool,covid_data:bool,news:bool) -> None:
    """
    Constructs a toast widget to display to the user in the UI

    Args: update_name - str, name of update
    update_time - str, time of update
    repeat - bool, will it repeat?
    covid_data - bool, update covid data?
    news - bool, update news articles?
    """

    try:
        #Creates a display string for content box on webpage
        content_string = ("Update set for: " + update_time)
        if repeat:
            content_string = (content_string + Markup('<br>') + "Update repeats")
        if covid_data:
            content_string = (content_string + Markup('<br>') + "Refreshes Covid-19 data")
        if news:
            content_string = (content_string + Markup('<br>') + "Refreshes news")

        #Places data into update template
        new_update = {
            'title': update_name,
            'content': content_string,
            'update_time': update_time,
            'repeat': repeat,
            'covid-data': covid_data,
            'news': news,
            }

        #Inserts update by time order
        display_update.append(new_update)
    #Raised when form returns a nonetype for one of the parameters
    #Critical as scheduling will break without new update appended to list
    except TypeError:
        logging.critical("Form returning a NoneType, cannot build toast")

#---------------DATA UPDATES

def update_covid_data(update_to_remove:dict) -> unschedule_update:
    """
    Updates all the covid-19 data displayed to the user on the UI

    Args: update_to_remove - Dictionary, When function is called it is
    normally by a scheduler, this arg is then used to remove the toast
    icon for that update in the UI

    Returns: unschedule_update - Function, removes update toast from UI and
    scheduler which has just been performed
    """

    global current_data
    current_data = formatted_all_data()

    logging.info('COVID-19 data updated')
    #Removes toast widget on dashboard as update is complete
    return unschedule_update(update_to_remove)



def update_current_articles(update_to_remove:dict) -> unschedule_update:
    """
    Updates the 5 articles displayed to the user

    Args: update_to_remove - Dictionary, When function is called it is normally by a
    scheduler, this arg is then used to remove the toast icon for that update in the UI

    Returns: unschedule_update - Function, removes update from UI which has just
    been performed
    """

    global current_articles
    current_articles = update_news()

    logging.info('News articles updated')
    #Removes toast widget on dashboard as update is complete
    return unschedule_update(update_to_remove)

def update_both(update_to_remove:dict) -> None:
    """
    Updates all data on the UI (Covid-19 data and News articles)

    Args: update_to_remove - Dictionary, When function is called it is normally by a
    scheduler, this arg is then used to remove the toast icon for that update in the UI
    """

    update_covid_data(update_to_remove)
    update_current_articles(update_to_remove)

def recursive_update(update_to_reschedule:dict) -> None:
    """
    When a user schedules an update to repeat this function is called. Every time the update
    time is reached it updates the chosen data and reschedules itself.

    Args: update_to_reschedule  - Dictionary, When function is called it is normally by a
    scheduler, this arg is then used to reschedule the update after being performed
    """

    logging.info('Repeated update rescheduling')
    #Removes update from list
    display_update.remove(update_to_reschedule)
    #Checks which data needs to be updated
    if update_to_reschedule['covid-data']:
        update_covid_data('')
    if update_to_reschedule['news']:
        update_current_articles('')

    #Enqueues update to back of the queue, this is done as scheduler assumes new
    #update being added is at the back of the queue
    display_update.append(update_to_reschedule)

    #Gets the update interval and reschedules update
    update_time = time_difference(update_to_reschedule['update_time'])
    schedule_covid_updates(update_time, recursive_update)


if __name__ == '__main__':
    app.run()
