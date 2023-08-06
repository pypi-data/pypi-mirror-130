"""
 COVID DATA HANDLER
 =======================

 Used to parse and extract csv data
 Uses Covid19 API to get covid data about location in england
 and format it to be displayed to users
"""

import json
import logging
import os
from uk_covid19 import Cov19API

#Loads the config data, to be used throughout the module (using abs path)
this_directory = os.path.dirname(__file__)
with open(os.path.join(this_directory, 'config.json'),encoding="utf-8") as f:
    config_data = json.load(f)


def parse_csv_data(csv_filename:str) -> list:
    """
    Extracts data from a csv file and parses each line into a list

    Args: csv_filename - String, The name of the csv file

    Return: string_list - List, List of each line in the csv file
    """

    string_list = []

    try:
        with open(csv_filename) as csv_file:
            #Loops through file adding each line to a list
            for line in csv_file:
                string_list.append(line)
    except FileNotFoundError:
        logging.warning('csv filename incorrect')

    return string_list


def process_covid_csv_data(covid_csv_data:list) -> tuple:
    """
    Takes in formatted csv data and finds hopsital cases, the num of infections
    from the last 7 days, and the total deaths

    Args: covid_csv_data - List, Formatted covid data from reading a csv file

    Return: Tuple, contains the 3 integers that are required to be extracted (described above)
    """

    try:
        #Current hospital case finder
        split_string = covid_csv_data[1].split(",")
        try:
            current_hospital_cases = int(split_string[5])
        except ValueError:
            logging.warning("Current hospital cases value cannot be converted to int")

        #Number of cases finder
        last7days_cases = 0
        #Disincludes the first data entry in the csv file
        for i in range(3,10):

            split_string = covid_csv_data[i].split(",")

            last7days_cases += int(split_string[6])

        #Total death finder
        covid_csv_data.pop(0)
        for i in covid_csv_data:

            split_string = i.split(",")
            #Conditional finds first nontype data entry for deaths
            if split_string[4] != "":

                total_deaths = int(split_string[4])
                break

        return last7days_cases, current_hospital_cases, total_deaths
    #Exception for if data could not be extracted, this may be raised if incorrect csv file used
    except IndexError:
        logging.warning("Index out of range, data could not be extracted")
        return None


def covid_API_request(location:str = config_data['location'],
location_type:str = config_data['location_type']) -> dict:
    """
    Using the NHS covidAPI, the filters and the return format are set up and
    then input as an API request. The data is then formatted

    Args:
    location - String, Location of the user, taken from config file
    location_type - String, The area type of that location, e.g. utla, ltla
    or nation

    Return: Dictionary (formatted like the variable cases_and_deaths)
    outputted from the covid19 API
    """

    #Paramaters used to filter the data
    #areaType ia a mandatory metric, must be defined in all queries
    filter_choice = [
        "areaType="+location_type,
        "areaName="+location
    ]

    #Format the data will output in
    cases_and_deaths = {
        "date": "date",
        "areaName": "areaName",
        "areaCode": "areaCode",
        "newCasesByPublishDate": "newCasesByPublishDate",
        "hospitalCases": "hospitalCases",
        "cumDailyNsoDeathsByDeathDate": "cumDailyNsoDeathsByDeathDate"
    }
    #Data requested from API
    api = Cov19API(filters=filter_choice, structure=cases_and_deaths)

    logging.info('Cov19API request successful!')
    try:
        data = api.get_json()

        return data
    #Exception makes sure API returning correct data, critical as
    #program unable to run without data
    except AttributeError:
        logging.critical('Cov19API returning incorrect data structure')
        return None


def national_data_API_extract() -> list:
    """
    Finds covid statistics required for the nation

    Return: stats - List, list of data about covid19 nationally
    """

    try:
        #Gets nation specified in config
        nation = config_data['nation']

        data = covid_API_request(nation, "nation")['data']

        stats = []
        #Relevant statistics are placed in a list
        stats.append(last7day_infections(data))
        stats.append(today_hospital_cases(data))
        stats.append(total_death_finder(data))

        return stats
    #Checks correct key is used for config data, only a .error as code will continue running
    except KeyError:
        logging.error('"nation" key not found in config data')
        return None
    #Critical as without data program cannot continue
    except AttributeError:
        logging.critical('Cov19API returning incorrect data structure')
        return None

def formatted_all_data() -> list:
    """
    Gets and formats both national and local covid data to be displayed in the dashboard

    Returns: formatted_data - list, list of relevant covid data, with strings to describe
    what the data is, this is displayed on the covid dashboard
    """

    formatted_data = []
    #Gets local data
    formatted_data.append(local_infection_extract())
    #Gets national data
    national_data = national_data_API_extract()

    try:
        #Strings are added to data, as will be displayed on a dashboard
        formatted_data.append(national_data[0])
        formatted_data.append('Hospital Cases: ' + str(national_data[1]))
        formatted_data.append('Deaths: ' + str(national_data[2]))

        logging.info('Covid data updated - Local infections: ' + str(formatted_data[0]) +
        ' National Infections: ' + str(formatted_data[1]) + ' ' + formatted_data[2]
        + ' ' + formatted_data[3])
    #Error as program can continue although data will be incorrect
    except IndexError:
        logging.error('Incorrect index for national data, data has not been properly updated')

    return formatted_data

def last7day_infections(data:list) -> int:
    """
    Finds the total cases of covid in the last 7 days

    Args: data - List of dictionaries containing covid data about each day

    Return: last7days_cases - Integer, Total cases in the last 7 days
    """

    try:
        last7days_cases = 0

        for i in range(0,7):
            last7days_cases += int(data[i]["newCasesByPublishDate"])

        return last7days_cases
    except IndexError:
        logging.error('Index out of range, no data for infections')
        return None


def today_hospital_cases(data:list) -> int:
    """
    Find the total number of hospital cases for the closest day to today with availale data

    Args: data - List of dictionaries containing covid data about each day

    Return: hospital_cases - Integer, Number of hospital cases on the given day
    """

    try:
        #Loop locates first day with data entry for hospital cases
        for day in data:

            if day['hospitalCases']:
                hospital_cases = int(day['hospitalCases'])
                break

        return hospital_cases
    except IndexError:
        logging.error('Index out of range, no data for hospital cases')
        return None
    except UnboundLocalError:
        logging.error('Data arg is of NoneType, no data available to extract cases')
        return None


def total_death_finder(data:list) -> int:
    """
    Finds the total number of deaths from the dictionary of data

    Args: data - List of dictionaries containing covid data about each day

    Returns: total_deaths - int, total covid deaths in a given reigon/nation
    """

    try:
        for day in data:
            #Cummulative deaths is null for first few entrys so
            #loop finds the first death count containing a value
            try:
                if day["cumDailyNsoDeathsByDeathDate"]:

                    total_deaths = day["cumDailyNsoDeathsByDeathDate"]
                    break
            except KeyError:
                logging.error('key does not exist, death data cannot be found')

        return total_deaths
    except IndexError:
        logging.error('Index out of range, no data for deaths')
        return None
    except UnboundLocalError:
        logging.error('Data arg is of NoneType, no data available to extract')
        return None


def local_infection_extract(location:str = config_data['location']) -> int:
    """
    Gets the number of infections in the last 7 days for the users local location

    Args: location - String, Users local location (default stored in config file)

    Return: infection_rate - Integer, The number of infections in the last 7 days
    """

    infection_rate = last7day_infections(covid_API_request(location)['data'])

    return infection_rate
