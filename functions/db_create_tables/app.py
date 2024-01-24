import json
import boto3
from helpers import *


def lambda_handler(event, context):
    
    # In practice, you probably won't set up the database this way. 
    # It's much more likely that you'd use the RDS query editer to create the tables.
    # But this might be useful if you're wanting to port your app to another AWS account.
    
    sql_statements = [
                "DROP TABLE if exists companies;",
                
                """CREATE TABLE companies (
                    id int primary key AUTO_INCREMENT,
                    name varchar(255) unique key);""",

                "DROP TABLE if exists people;",

                """CREATE TABLE people (
                    id int primary key AUTO_INCREMENT,
                    first varchar(100),
                    last varchar(100),
                    email varchar(100),
                    phone varchar(20),
                    dob date,
                    unique key (first, last, dob));"""
                    ]
        
    for sql in sql_statements:
        r = execute_statement(sql)

    return r