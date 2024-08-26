import json
import boto3
import os
import logging
import random
import string

sqs_url = os.environ["SQS_URL"]
logger = logging.getLogger()
logger.setLevel("INFO")

def data_generator():
    message = {
        "bookingId":str(random.randint(10000,99999)) ,
        "userId":''.join(random.choices(string.ascii_uppercase + string.digits, k = 10)),
        "propertyId":''.join(random.choices(string.ascii_uppercase + string.digits, k = 10)),
        "location":random.choice(["Tampa, Florida","Hyd, Ind","BLR, Ind"]),
        "startDate":random.choice(["2024-03-12","2024-03-13","2024-03-14"]),
        "endDate":random.choice(["2024-03-13","2024-03-14","2024-03-15"]),
        "price":'$ ' +  str(random.randint(100,999))
    }
    return message

def lambda_handler(event, context):
    sqs_client = boto3.client('sqs')
    for i in range(5):
        messagedata = json.dumps(data_generator())
        sqs_client.send_message(QueueUrl = sqs_url, MessageBody = messagedata)
        logger.info("Published Message to Queue: " + messagedata)