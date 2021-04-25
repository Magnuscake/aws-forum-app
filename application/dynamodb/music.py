import json
import os
from decimal import Decimal

import boto3

# Define the service resource and client globally
dynamodb = boto3.resource('dynamodb')
dynamodb_client = boto3.client('dynamodb')

def create_music_table():
    try:
        table = dynamodb.create_table(
            TableName='Music',
            KeySchema=[
                {
                    'AttributeName': 'artist',
                    'KeyType': 'HASH'
                },
                {
                    'AttributeName': 'title',
                    'KeyType': 'RANGE'
                }
            ],
            AttributeDefinitions=[
                {
                    'AttributeName': 'artist',
                    'AttributeType': 'S'
                },
                {
                    'AttributeName': 'title',
                    'AttributeType': 'S'
                },
            ],
            ProvisionedThroughput={
                'ReadCapacityUnits': 5,
                'WriteCapacityUnits': 5
            }
        )

        # Wait until the table exists.
        table.meta.client.get_waiter('table_exists').wait(TableName='Music')

        with open("./application/dynamodb/a2.json") as json_file:
            music_data = json.load(json_file, parse_float=Decimal)
        load_music_data(music_data)

    except dynamodb_client.exceptions.ResourceInUseException:
        print("This table already exists")

    #  print(os.path.dirname(__file__))

def load_music_data(music_data):
    table = dynamodb.Table('Music')
    for music in music_data['songs']:
        table.put_item(Item=music)

def get_artist_urls():
    scan_kwargs = {
        'ProjectionExpression': "img_url"
    }

    table = dynamodb.Table('Music')
    response = table.scan(**scan_kwargs)

    artist_img_urls = {item['img_url'] for item in response['Items']}

    return artist_img_urls
