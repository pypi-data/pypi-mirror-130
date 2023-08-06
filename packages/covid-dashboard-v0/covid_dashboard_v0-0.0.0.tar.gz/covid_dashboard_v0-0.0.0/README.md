# COVID-19 Dashboard
**Author**: Oscar Klemenz 

**Github**: https://github.com/OscarKlemenz/covid_dashboard

**Pypi**: https://pypi.org/user/OscarKlemenz/

**Python version** : Python 3.9
## Introduction 
This application is a dashboard displaying statistics about COVID-19 in the UK, and complementary news articles about current events. It has been created to inform users about important COVID-19 statistics throughout the nation and in their local area. Furthermore, users can schedule updates to the data allowing for live feedback about current events. 

Technologies used:
- This application was created using the NHS Covid-19 API. This is used to get statistics about Covid-19 in the UK
- NewsAPI was also used to get articles from across the web to display to the user. 

Throughout this project I faced many challenges, but one that sticks out is the development of scheduled updates. This was a challenge as this was my first project using the sched module. 
Furthermore, scheduling updates involved learning how to check for updates in parallel to the rest of my application code. 
Although this was a challenge, to be able to complete this feature was rewarding. It has also helped me develop an understanding for scheduling, which was a new topic to me. 

In future I plan on implementing graphical representations of Covid-19 data, as through visualising the data it can be better understood. Moreover, I plan to allow the user to change the terms used for the news search in runtime, allowing them to explore articles on different topics. 

## Dependencies 

- requests 
- uk-covid19
- flask
- pytest
- pylint

## Installation 

To install modules follow the guidance in the url - https://docs.python.org/3/installing/index.html

## Getting Started
### Accessing the dashboard
Firstly, to run the dashboard, you will need to get an API key from the NewsAPI (https://newsapi.org). Your unique key will allow you to access news articles in the dashboard. Place your API key inside the config.json file as the value for the key 'apiKey'

To launch the dashboard, open the terminal in the directory:

    /covid_dashboard/covid_dashboard

Once a terminal is open at this directory, run these commands: 

    > source .virtualenv/bin/activate
    > pip install -r requirements.txt
    > python app.py

Once app.py is running, go to the url http://127.0.0.1:5000 to access the dashboard. 
### Navigating the dashboard
Covid-19 data is displayed in the center of the UI and news articles are located to the right. 
To schedule new updates enter your paramaters into the form, the time entered into this form will then be the time the update occurs. 
Updates and news articles can be removed by clicking on the cross icon on each widget. 
### Personalising the dashboard 
The dashboard can be customised for each user by altering the values in config.json. Values that can altered are listed below:
- **Location**: The name of you local town/city
- **Location-type**: Possible location types are ltla, utla and reigon. Test each one until you find which works for your data. 
- **Nation**: Your nation within the UK
- **defaultNewsTerms**: Keywords news articles should contain. Seperate each term with a space. 
- **newsLanguage**: Language the news articles should be in. 

## Testing 
Due to this application using external APIs, in time they may be updated affecting the ability to run this application. 

Functions within this application can be tested using pytest the corresponding test modules listed below:
- test_app.py
- test_covid_data_handler.py
- test_news_data_handler.py 

To run pytest, first launch the virtual environment explained in the getting started section and in the terminal run these lines:

    > source .virtualenv/bin/activate
    > pytest

Pytest will then perform tests and output the results
## Developer documentation
For those wishing to contribute to this application, docstrings for each function can be accessed inside the docs folder of this package.

Docstring path:

    covid_dashboard/docs/_build/html/index.html

The source code of this application can be accessed at:

- Github: https://github.com/OscarKlemenz/covid_dashboard
- Pypi: https://pypi.org/user/OscarKlemenz/