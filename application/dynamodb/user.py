import os
import logging
import json
from decimal import Decimal

import boto3
from boto3.dynamodb.conditions import Key, Attr

# Define the service resource and client globally
dynamodb = boto3.resource('dynamodb')
dynamodb_client = boto3.client('dynamodb')

def put_user(email, username, password):
    table = dynamodb.Table('User_Details')

    response = table.put_item(
        Item = {
            'email': email,
            'username': username,
            'password': password
        }
    )

    return response

def key_exists(key, user_input):
    table = dynamodb.Table('User_Details')

    response = table.query(
        KeyConditionExpression = Key(key).eq(user_input)
    )

    if response['Items']:
        return True

    return False

def attr_exists(attribute, user_input):
    table = dynamodb.Table('User_Details')

    response = table.scan(
        FilterExpression = Attr(attribute).eq(user_input)
    )

    if response['Items']:
        return True

    return False

def login_user(email, password):
    table = dynamodb.Table('User_Details')

    response = table.get_item(
        Key={
            'email': email
        }
    )

    item = response['Item']

    if not item['password'] == password:
        return None

    return item

def create_users():
    table = dynamodb.Table('User_Details')

    try:
        base_dir = os.path.dirname(__file__)
        abs_file = os.path.join(base_dir, 'users.json')

        with open(abs_file) as json_file:
            users = json.load(json_file, parse_float=Decimal)

            for user in users['users']:

                response = table.query(
                    KeyConditionExpression = Key('email').eq(user['email'])
                )

                if not response['Items']:
                    table.put_item(Item=user)

    except dynamodb_client.exceptions.ResourceNotFoundException as e:
        logging.error(e)

