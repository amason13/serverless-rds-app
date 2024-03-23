# Import any modules you need here
import boto3
import json
import os
from datetime import datetime, timedelta


# Import environment variables here - as set up in template.yaml file
# we can call them once here and don't need to call them in each function
S3_BUCKET = os.environ['S3_BUCKET']
DATABASE_NAME = os.environ['DATABASE_NAME']
DB_CLUSTER_ARN = os.environ['DB_CLUSTER_ARN']
DB_CREDENTIALS_SECRETS_STORE_ARN = os.environ['DB_CREDENTIALS_SECRETS_STORE_ARN']

# Create an RDS client
rds_client = boto3.client('rds-data')

#################################
##### Some useful functions #####
#################################

# function to execute single sql statement using RDS serverless data api
def execute_statement(sql, sql_parameters=[]):
    response = rds_client.execute_statement(secretArn=DB_CREDENTIALS_SECRETS_STORE_ARN,
                                            database=DATABASE_NAME,
                                            resourceArn=DB_CLUSTER_ARN,
                                            sql=sql,
                                            parameters=sql_parameters)
        
    response_object = {}
    response_object['isBase64Encoded']=False
    response_object['statusCode'] = response['ResponseMetadata']['HTTPStatusCode']
    response_object['headers'] = {}
    response_object['headers']['Content-Type']='application/json'
    response_object['headers']['Access-Control-Allow-Origin']='*'
    response_object['multiValueHeaders'] = {}   
    response_object['body'] = json.dumps(response)     
    return response_object

# function to BATCH execute sql statement using RDS serverless data api
def batch_execute_statement(sql, sql_parameter_sets):
    response = rds_client.batch_execute_statement(secretArn=DB_CREDENTIALS_SECRETS_STORE_ARN,
                                                database=DATABASE_NAME,
                                                resourceArn=DB_CLUSTER_ARN,
                                                sql=sql,
                                                parameterSets=sql_parameter_sets)
    response_object = {}
    response_object['isBase64Encoded']=False
    response_object['statusCode'] = response['ResponseMetadata']['HTTPStatusCode']
    response_object['headers'] = {}
    response_object['headers']['Content-Type']='application/json'
    response_object['headers']['Access-Control-Allow-Origin']='*'
    response_object['multiValueHeaders'] = {}
    response_object['body'] = json.dumps(response)
    return response_object

# execute GET sql statement using RDS serverless data api
def execute_get_statement(sql):
    response = rds_client.execute_statement(
        secretArn=DB_CREDENTIALS_SECRETS_STORE_ARN,
        database=DATABASE_NAME,
        resourceArn=DB_CLUSTER_ARN,
        sql=sql, 
        includeResultMetadata=True)
    
    data = []
    column_names = [el['label'] for el in response['columnMetadata']]
    rows = [[list(r.values())[0] for r in row] for row in response['records']]
    
    for i in range(len(rows)):
        data.append(dict(zip(column_names, rows[i])))        
        
    response_object = {}
    response_object['isBase64Encoded']=False
    response_object['statusCode'] = 200
    response_object['headers'] = {}
    response_object['headers']['Content-Type']='application/json'
    response_object['headers']['Access-Control-Allow-Origin']='*'
    response_object['multiValueHeaders'] = {}
    response_object['body'] = json.dumps(data)
    
    return response_object

def log_values(table_name, id_):
    # log what is being deleted
    select_response = rds_client.execute_statement(secretArn=DB_CREDENTIALS_SECRETS_STORE_ARN,
                                                    database=DATABASE_NAME,
                                                    resourceArn=DB_CLUSTER_ARN,
                                                    sql="SELECT * FROM {} WHERE id={}".format(table_name, id_),
                                                    includeResultMetadata=True)

    col_names = [el['name'] for el in select_response['columnMetadata']]
    values = [list(el.values())[0] for el in select_response['records'][0]]
    print("Values before modification/deletion: {}".format(dict(zip(col_names, values))))

# function to read object from s3
def get_object_from_s3(bucket, key):
    s3 = boto3.resource('s3')
    obj = s3.Object(bucket, key)
    return obj.get()['Body'].read().decode('utf-8')

# function to write object to s3
def write_object_to_s3(bucket, key, data):
    s3 = boto3.resource('s3')
    obj = s3.Object(bucket, key)
    obj.put(Body=data)
    return True

# Use this as a template for each helper function you write. 
# Include an indicator as to what data type will be output '->int' in this case.
# Include a detailed docstring so everyone else knows what the function does.
# Include section by section descriptions of what the function does.
def template_function(x, y, z)->int:
    """Example function to output the sum of three integer parameters passed in.

    Parameters
    ----------
    x : int
        first integer
    y: int
        next integer to add
    z: int
        final integer to add

    Returns
    -------
    out : int
        Sum of all three integers passed into the function."""
    
    # Sum all three variables
    out = x+y+z

    return out