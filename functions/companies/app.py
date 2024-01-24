import json
import boto3
from helpers import *
import requests

TABLE_NAME = 'companies'

def lambda_handler(event, context):
    # logging
    print('event:')
    print(event)

    ### Get data from db
    if event['httpMethod']=='GET':
        # extract parameters
        if 'id' in event['queryStringParameters']:
            id_ = int(event['queryStringParameters']['id'])
            sql = f" SELECT * from {TABLE_NAME} where id={id_} "
        else:
            sql = f" SELECT * from {TABLE_NAME} limit 10000"

        return execute_get_statement(sql)

    ### Add data to db
    elif event['httpMethod']=='POST':
        # extract parameters
        body = json.loads(event['body'])
        name = body['name']

        # insert values into table
        sql = f"INSERT INTO {TABLE_NAME} (name) values ('{name}')"
        return execute_statement(sql)

    ### Change data in db
    elif event['httpMethod']=='PUT':
        # extract parameters
        body = json.loads(event['body'])
        id_ = int(body['id'])
        name = body['name']

        # log values which are about to be deleted/modified to cloudwatch
        log_values(TABLE_NAME, id_)

        # update values in table
        sql = f" UPDATE {TABLE_NAME} SET name='{name}' WHERE id={id_} "
        return execute_statement(sql)

    ### Delete data from db
    elif event['httpMethod']=='DELETE':
        # get query string parameters
        id_ = int(event['queryStringParameters']['id'])

        # log values which are about to be deleted/modified to cloudwatch
        log_values(TABLE_NAME, id_)

        sql = f" DELETE from {TABLE_NAME} where id={id_} "
        resp = execute_statement(sql)

       return resp

    else:
        response_object = {}
        response_object['isBase64Encoded']=False
        response_object['statusCode'] = 400
        response_object['headers'] = {}
        response_object['headers']['Content-Type']='application/json'
        response_object['headers']['Access-Control-Allow-Origin']='*'
        response_object['multiValueHeaders'] = {}
        return response_object