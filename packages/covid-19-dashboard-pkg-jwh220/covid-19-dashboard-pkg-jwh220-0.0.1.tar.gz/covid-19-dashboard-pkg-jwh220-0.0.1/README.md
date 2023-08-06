# COVID-19 Dashboard

## Table of Contents
- [Introduction](##Introduction)
- [Prerequisites](##Prerequisites)
- [Instalation](##Instalation)
- [Getting Started](##Getting-Started)
- [Testing](##Testing)
- [Developer Documentation](##Developer-Documentation)
- [Details](##Details)

## Introduction:
Creates a locally hosted webpage containing COVID-19 data and news:
- local last 7 days infection rate
- national last 7 days infection rate
- national current hospital cases
- national total deaths (from COVID-19)

## Prerequisites
- Python 3.10.0 64-bit
- Python sched module
- Python time module
- Python json module
- Python logging module
- Python flask module
- Python markupsafe module
- uk_covid19 module (infomation [here](https://publichealthengland.github.io/coronavirus-dashboard-api-python-sdk/pages/getting_started.html))
- newsapi module (infomation [here](https://newsapi.org/))

## Instalation
- `pip install x`

## Getting Started
- In the file 'config.json', add your [API key](https://newsapi.org/) where it says "**news API key here**"
- Run the package
    - There will be no visual confirmation that it is running successfully
- In a web browser go to http://127.0.0.1:5000/
- ### Adding update
    ![Screenshot of bottom middle part of webpage](static/images/add_update.png)
    - Add the time of the update to the top input box (where it says '12:30')
    - Add the name of the update to the second input box (where it says 'Update label')
    - If you want the update to happen every 24-hour, check the 'Repeat update' box; if it is a one-off, leave it unchecked
    - Depending if you want to update the COVID-19 data or news, check the relevant boxes ('Update Covid data' or 'Update news articles')
        - If neither box is checked, the update will not be set
        - Both boxes can be checked at once, creating an update for the data and news uder the same name
        - New updates can't be set for the same time as scheduled updates
    - Press the 'Submit' button to create your new update (as the number of visible updates is limited to the next 5, you may not see the update appear instantly)
- ### Remove update
    ![Screenshot of top left part of webpage](static/images/remove_update.png)
    - Click on the cross on the top right of an update to remove it
        - If you have a news and data update, like 'example combiation', there is no way to remove just the data or news update
- ### Remove news article
    ![Screenshot of top left part of webpage](static/images/remove_news.png)
    - Click on the cross on the top right of a news article to remove it

## Testing
- Enter a terminal
- Navigate to the folder conataining this
- Run `pytest` (infomation [here](https://docs.pytest.org/en/6.2.x/getting-started.html))

## Developer Documentation
- ### config.json
    - api_key : string
        - add your newsapi key here
    - news_search_terms : string
        - add any search terms you want headlines for, separated by a space for multiple search terms
        - default searches for covid-19 related news
    - location : string
    - location_type : string
        - add your chosen area here
        - see valid filters [here](https://coronavirus.data.gov.uk/details/developers-guide/main-api#params-filters)
    - updates : list
        - a list of updates to add when start, formatted like an update (see below)
    - update : dictionary
        - a preset update to be added to the page
        - name : string
            - the name of the update
        - time : string in format "HH:MM" or float
            - the time of day the update should occur ("HH:MM") **_OR_**
            - the amount of time (in seconds) from startup to the update
        - type : string
            - the type of update
            - "data" for data update
            - "news" for news update
            - "both" for data and news update
        - repeat : string
            - whether the update should repeat every 24 hours
            - "False" for single update
            - "True" for repeating update
    - web_title : string
        - the title of the page
    - language : string
        - the language of articles that should be fetched (see valid options [here](https://newsapi.org/sources))

## Details
- Made by Joshua Hammond
- Shared under MIT (see [LISENSE](LICENSE))
- Source code can be found [here](https://github.com/Peter-Bread/CS-Programming-Module-Current)
