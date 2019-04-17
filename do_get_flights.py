import json
import requests
import os
import re
import pprint
import pickle

## This is the base url for requesting flights from skiscanner api
apiUrlBase = 'https://skyscanner-skyscanner-flight-search-v1.p.rapidapi.com/apiservices/browsequotes/v1.0/US/USD/en-US/'

headers = {'RapidAPI Project': 'default-application_3730232',
           'X-RapidAPI-Key': 'c16364fc2bmsh11edc29fd4f0b65p190c41jsn664944a5cb5c'}

## This dictionary is loaded from a list of all cities around the world that have airports,
## can be updated via update_city_codes.py

def updateCityDict():
    with (open("data/cityDict.pkl", "rb")) as openfile:
        while True:
            try:
                cityDict = pickle.load(openfile)
            except EOFError:
                break
    return cityDict

################################
## Request and retrieve data ###
################################
def make_url(city):
    ##Later modify this so that given a city it will
    ##search for cities within given driving distance and then return a
    ##url for all of them??
    try: cityDict
    except NameError: cityDict = updateCityDict()
    return apiUrlBase + cityDict[city] +"/anywhere/anytime"

def get_flight_info(city):
    apiUrl = make_url(city)
    print("Requesting: "+apiUrl)
    response = requests.get(apiUrl, headers=headers)

    if response.status_code == 200:
        data = json.loads(response.content.decode('utf-8'))
        return data['Quotes'],data['Carriers'], data['Places']
    else:
        print("Error retrieving: "+city)
        return None

#######################
## View/Save Results ##
#######################
def show_query(city):
    flightInfo = get_flight_info(city)

    if flightInfo is not None:
        print("Here's your info: ")
        pprint.pprint(flightInfo)

    else:
        print('[!] Request Failed')

def save_search(data):
    with open("data_file.json", "w") as write_file:
        json.dump(data, write_file)
    json.dumps(data, indent=4)
    return
