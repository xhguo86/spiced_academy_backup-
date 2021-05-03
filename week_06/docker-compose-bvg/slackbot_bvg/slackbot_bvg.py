import time
import pandas as pd
import requests
from sqlalchemy import create_engine
from sqlalchemy.sql import select
import config

time.sleep(30)
conn_str = 'postgresql://postgres:1234@my_postgres:5432/my_bvg_data'
engine = create_engine(conn_str, echo=True)

query_late='''
    SELECT running_time, delay, name
    FROM s_koepenick_timetable
    WHERE delay > 10
    ORDER BY running_time DESC
'''

late= pd.read_sql(query_late, engine).drop_duplicates()
late['running_time']=pd.to_datetime(late['running_time'])

text1= "There will be a delay of {delay} minutes on the line {name} from S-Bahn Köpenick at {my_time} on {my_day}.".format(delay=round(int(late.at[0, 'delay'])/60), name=late.at[0, 'name'], my_time=str(late.at[0, 'running_time'].hour)+":"+str(late.at[0, 'running_time'].minute), my_day=str(late.at[0, 'running_time'].day)+" "+ str(late.at[0, 'running_time'].strftime("%B")))

text2= "There will be a delay of {delay} minutes on the line {name} from S-Bahn Köpenick at {my_time} on {my_day}.".format(delay=round(int(late.at[1, 'delay'])/60), name=late.at[1, 'name'], my_time=str(late.at[1, 'running_time'].hour)+":"+str(late.at[1, 'running_time'].minute), my_day=str(late.at[1, 'running_time'].day)+" "+ str(late.at[1, 'running_time'].strftime("%B")))

text3= "There will be a delay of {delay} minutes on the line {name} from S-Bahn Köpenick at {my_time} on {my_day}.".format(delay=round(int(late.at[2, 'delay'])/60), name=late.at[2, 'name'], my_time=str(late.at[2, 'running_time'].hour)+":"+str(late.at[2, 'running_time'].minute), my_day=str(late.at[2, 'running_time'].day)+" "+ str(late.at[2, 'running_time'].strftime("%B")))

WEBHOOK_URL = "https://hooks.slack.com/services/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" 
#WEBHOOK_URL = config.WEBHOOK_URL
lst = [text1, text2, text3]
text = "\n".join(lst)
json_payload = {'text': text}

requests.post(url=WEBHOOK_URL, json = json_payload)