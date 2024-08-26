import json
import boto3
import os
from datetime import date
import io
import pandas as pd
import logging

bucket_name = os.environ["Bucket_Name"]
logger = logging.getLogger()
logger.setLevel("INFO")

def lambda_handler(event, context):
    # print('Event: ',event)
    # print('Context: ', context)
    message = event[0]['body']
    s3_client = boto3.client('s3')
    s3_resource = boto3.resource('s3')
    today_date = str(date.today())
    print(message)
    if (message == {}):
        return {}
    try:
        logger.info('Entering Try Fn')
        obj = s3_client.get_object(Bucket = bucket_name, Key = f'date={today_date}/Airbnb_{today_date}.csv' )
        obj = obj['Body'].read()
        logger.info("File exists")
        s=str( obj ,'utf-8')
        data = io.StringIO(s)
        df=pd.read_csv(data,index_col='bookingId')
        df.loc[message['bookingId']] = [message['userId'],message['propertyId'],
                                    message['location'],message['startDate'],message['endDate'],
                                    message['price']]  
        df.to_csv('/tmp/test.csv',encoding='utf-8')
        s3_resource.Bucket(bucket_name).upload_file('/tmp/test.csv',f'date={today_date}/Airbnb_{today_date}.csv')
        print(df)
    except Exception as e:
        logger.info("Error: " + str(e))
        df = pd.DataFrame(columns = ['bookingId','userId','propertyId','location','startDate','endDate','price'])
        df = df.set_index(list(df.columns)[0])
        df.loc[message['bookingId']] = [message['userId'],message['propertyId'],
                                message['location'],message['startDate'],message['endDate'],
                                message['price']]  
        df.to_csv('/tmp/test.csv',encoding='utf-8')
        s3_resource.Bucket(bucket_name).upload_file('/tmp/test.csv',f'date={today_date}/Airbnb_{today_date}.csv')