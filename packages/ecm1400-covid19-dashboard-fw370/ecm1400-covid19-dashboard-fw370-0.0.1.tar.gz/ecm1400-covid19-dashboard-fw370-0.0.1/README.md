# README User Manual

## Introduction:

This Python project receives the latest COVID-19 Data for the COVID-19 outbreak in the United Kingdom using the publichealthengland COVID-19 API Service. We also receive COVID-19 relevant news from newsapi.org. This data is then displayed on a localhost webpage that allows users to view the data and schedule data updates, acting as a COVID-19 dashboard. This project was built for the purpose of ECM1400 Programming Continuous Assessment. 

### Prerequisites:

Python 3.10.0 used for development of this project. Visit https://python.org/downloads/ on a web browser to install.

### Installations:

###### All should be installed within the project environment.

Flask: A micro web framework that allows us to localhost a webpage. 

```
$ pip install Flask
```

Uk-covid19: Library used for retrieving the latest COVID-19 Data.

```
$ pip install uk-covid19
```

pytest: Used to test the code and ensure it is working correctly.

```
$ pip install -U pytest
```



### Getting started:

With python 3.10.0 installed and both Flask and uk-covid19 also installed, we may now make a start running the project. First step is obtaining a API key for the newsapi.org. If you do not already have an active API key for newsapi.org , visit https://newsapi.org/register to register for an API key. Once you have obtained your own API key, navigate to config.json within the python package and paste the API key within the apikey dictionary.

```json
{"apikey": [{"apikey": "Paste API key here"}]}
```

With the API key set, we may now run the project. To do this, we must open the command line terminal, navigate to the folder in which the package is located

```
cd C:\example
```

 and enter the following commands (assuming the python file containing Flask is named main.py)

```
set FLASK_APP=main
set FLASK_ENV=development
flask run
```

If we have a successful launch of main.py, we should see:

```
* Serving Flask app 'main' (lazy loading)
* Environment: development
* Debug mode: on
* Restarting with stat
* Debugger is active!
* Debugger PIN: xxx-xxx-xxx
* Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)
```

The final line in the terminal tells us where to visit to see our project working. Open a web browser and enter http://127.0.0.1:5000/index which will lead us to a localhost webpage running the template and code.

From this webpage, a client may schedule data and news updates. In the centre column of the page, below the COVID-19 data, is a series of forms to allow updates to be scheduled. Filling these in and pressing the submit button will call this and an update will be scheduled. 

To finish running the localhost webpage, simply press CTRL+C in the terminal. 

### Testing:

To run the tests provided within test_ecm1400.py, navigate to the project directory within terminal and enter the following command (assuming the test file has not been renamed):

```

pytest test_ecm1400.py
```

Pytest will respond with how many tests have passed, and if any tests have failed have specified which one(s). Each test has logging built in and will record whether the test passed or failed within the logging file.

##### test_config():

This test checks whether the config file returns a dictionary when loaded. If the config file does not return a dictionary, the data within will not be accessed properly. 

### Developer Details:

##### Files contained within the package:

nation_2021-10-28.csv : Contains the CSV data for parse_csv_data and process_csv_data functions within covid_data_handler.

config.json: Config file used to enter api key and edit default arguments.

covid_data.json: Stores the covid data from covid_data_handler.py

covid_news.json: Stores the news updates from covid_news_handling.py

scheduled_updates.json: Stores what updates are scheduled.

covid_data_handler.py: Retrieves data from the publichealthengland API.

covid_news_handling.py: Retrieves Covid-19 data from newsapi.org

test_ecm1400.py: Contains the testing functions to use with pytest.

app.py: The main file of the code. This is where the code is executed from.

README.md: This file, containing information on the project.

Templates folder containing index.html: Frontend for the Covid-19 Dashboard.

ecm1400_logging: Contains logged information on the status of the executed code.

##### Usage of the code:

The config file allows the API key along with the default search parameters for the news API and Covid-19 data API to be entered. For multiple terms in covid_terms whitespace should separate each term. The other json files should not be edited manually as the executed code will do so correctly.

##### Explanation of each function:

###### Functions within covid_data_handler.py:

###### parse_csv_data:

Reads data from a specified file and returns it in a list.

Opens a csv file with the name given as an argument, and appends an empty list with each item
being seperated by a newline in the csv file.

Parameters:
csv_filename (str) Provides the name of the desired csv file to open.

Returns:
covid_csv_data: A list of data separated by newline.

###### process_covid_csv_data:

Manipulates the list provided from the given argument and returns desired varaibles.

Creates two items, an empty list and an integer variable. Splits each item in the list again
by seperating between commas to create a nested list. Deletes first two items due to them
being useless. Assigns the required integer data to named variables.

Parameters:
covid_csv_data: List of covid data returned from the function "parse_csv_data".

Returns:
last7days_cases (int): Integer value of the Covid cases for the previous week.
current_hospital_cases (int): Integer value of the number current number of patients
hospitalised with Covid-19.
total_deaths (int): Total Number of Deaths due to Covid-19.

###### covid_API_request:

Requests certain data from the Cov19API and writes to a file.

Requests Covid-19 data as a json from the publichealthengland Cov19API/uk_covid19 module
before reading the json as a dictionary object and assigning the most recent data to named
variables. Finally writes this data into a JSON file
for permanence across modules and functions.

Parameters:
location (str): Provides areaName for the covid19API structure, with default value "Exeter".
location_type (str): Provides areaType, with default value "ltla".

Returns:
covid_data.json: "Returns" a json file with the desired data.

###### schedule_covid_updates:

Uses sched module to run functions with a delay of a desired time in seconds

Runs the function "covid_API_request" in a delay given. If a repeat is called
from the client side through flask requests, then the function will schedule
another call of the same function 24 hours from the originally scheduled time.

Parameters:
update_interval (int): Specifies the desired delay.
update_name (str): Specifies the name of the scheduled event.
repeat_update (str): Used to call a repeat of the scheduled update.

###### news_API_request:

Retrieves Covid News from newsapi and writes it into a json file.

First retrieves the apikey from a config json file. Specifies some parameters for the
requests function, which retrieves covid news titles and a short description of each
article_update from the newsapi. Writes this news in json format to
a file named 'covid_news.json'.

Parameters:
covid_terms (str): used in the query line of the newsapi to only return covid data.

Returns:
news_articles: Writes to a json formatted file.

###### update_news: 

Working in the same way as schedule_covid_updates, uses sched module to run functions with a delay of a desired time in seconds.

Runs the function "news_API_request" in a delay given. If a repeat is called
from the client side through flask requests, then the function will schedule
another call of the same function 24 hours from the originally scheduled time.

Parameters:
update_interval (int): Specifies the desired delay.
update_name (str): Specifies the name of the scheduled event.
repeat_update (str): Used to call a repeat of the scheduled update.

###### @app.route('/index', methods = ['GET']):

This specifies the URL of the flask template to run index on. Methods refers to the method used to retrieve client side information. In this case it is GET, which sends a message to the server which in response returns data.

###### index:

This function links the HTML template and the data processed from python.
    

Opens the two json files containing desired data and assigning them to variables
to be rendered in the template. Then uses requests.get to retrieve client side
inputs from the flask. Using these retrieved inputs and if statements,
the code responds accordingly to what has been requested by the client.

Return:
A built-in function that renders the HTML template by matching HTML variables
and python variables.

### Details:

Author: Frederick Westhead
Index.html template written by Matt Collison
License: MIT Licence



