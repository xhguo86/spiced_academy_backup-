"""
Berlin public transport API
documentation: https://v5.vbb.transport.rest/
"""

import requests
from pprint import pprint
import pymongo
import time
import logging

conn = pymongo.MongoClient('my_mongodb')
db = conn.infobvg


BASE_URL = 'https://v5.vbb.transport.rest'

# find a station
name = 'koepenick'
url = f"{BASE_URL}/locations?poi=false&addresses=false&query={name}"
j = requests.get(url).json()
closest_match = j[0]

pprint(closest_match['name'] + ' has id: ' + str(closest_match['id']))

# look up departures
print('\nNext connections from Köpenick:\n')

station_id = '900000180001'
mins = 10

url = f'{BASE_URL}/stops/{station_id}/departures?duration={mins}'

while True:
    j = requests.get(url).json()
    #for e in j:
        #print(e['plannedWhen'][11:-9], '  ', e['line']['name'], e['direction'])
    db.koepenick.insert_many(j)
    #logging.critical('Python script is still alive: ' + time.asctime())
    time.sleep(600)