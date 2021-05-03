import pandas as pd
import pymongo
import time
from sqlalchemy import create_engine

client =pymongo.MongoClient("my_mongodb")
db = client.infobvg
collection = db.koepenick

time.sleep(10)

entries = collection.find()

pg = create_engine('postgresql://postgres:1234@my_postgres:5432/my_bvg_data', echo=True)

pg.execute('''
    CREATE TABLE IF NOT EXISTS s_koepenick_timetable (
    running_time VARCHAR,
    delay VARCHAR,
    type VARCHAR,
    number VARCHAR,
    direction VARCHAR,
    name VARCHAR,
    mode VARCHAR
);
''')

for entry in entries:
    running_time = entry['when']
    delay = entry['delay']
    type = entry['line']['type']
    number = entry['line']['fahrtNr']
    direction = entry['direction']
    name = entry['line']['name']
    mode = entry['line']['mode']
    query = "INSERT INTO s_koepenick_timetable VALUES (%s, %s, %s, %s, %s, %s, %s);"
    pg.execute(query, (running_time, delay, type, number, direction, name, mode))


# Cleaning the data in the table
clean1_query = "ALTER TABLE s_koepenick_timetable ALTER COLUMN running_time TYPE TIMESTAMP WITHOUT TIME ZONE USING running_time::timestamp without time zone"
clean2_query = "ALTER TABLE s_koepenick_timetable ALTER COLUMN delay TYPE INT USING delay::integer"


pg.execute(clean1_query)
pg.execute(clean2_query)
