import json
import boto3
from helpers import *
import requests

TABLE_NAME = 'people'

def lambda_handler(event, context):
    
    # logging
    print('event:')
    print(event)

    ### Get data from db
    if event['httpMethod']=='GET':
        # extract parameters

        if event['queryStringParameters'] and 'id' in event['queryStringParameters']:
            id_ = int(event['queryStringParameters']['id'])
            sql = f" SELECT * from {TABLE_NAME} where id={id_} "

        else:
            sql = f" SELECT * from {TABLE_NAME} limit 10000"

        return execute_get_statement(sql)

    ### Add data to db
    elif event['httpMethod']=='POST':
        # extract parameters
        body = json.loads(event['body'])
        first = body['first']
        last = body['last']
        email = body['email']
        phone = body['phone']
        dob = body['dob']

        # insert values into table
        sql = f"""INSERT INTO {TABLE_NAME} (first,last,email,phone,dob) 
                values ('{first}','{last}','{email}','{phone}','{dob}')"""

        return execute_statement(sql)


    ### Change data in db
    elif event['httpMethod']=='PUT':
        # extract parameters
        body = json.loads(event['body'])
        id_ = int(body['id'])
        first = body['first']
        last = body['last']
        email = body['email']
        phone = body['phone']
        dob = body['dob']

        # log values which are about to be deleted/modified to cloudwatch
        log_values(TABLE_NAME, id_)
        
        # update values in table
        sql = f""" UPDATE {TABLE_NAME} SET first='{first}',
                                            last='{last}',
                                            email='{email}',
                                            phone='{phone}',
                                            dob='{dob}'
                                    WHERE id={id_} """
        return execute_statement(sql)


    ### Delete data from db
    elif event['httpMethod']=='DELETE':
        # get query string parameters
        id_ = int(event['queryStringParameters']['id'])

        # log values which are about to be deleted/modified
        log_values(TABLE_NAME, id_)

        sql = f" DELETE from {TABLE_NAME} where id={id_} "
        return execute_statement(sql)
        

    else:
        response_object = {}
        response_object['isBase64Encoded']=False
        response_object['statusCode'] = 400
        response_object['headers'] = {}
        response_object['headers']['Content-Type']='application/json'
        response_object['headers']['Access-Control-Allow-Origin']='*'
        response_object['multiValueHeaders'] = {}
        return response_object