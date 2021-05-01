import json
import os
from decimal import Decimal

import boto3
from boto3.dynamodb.conditions import Key, Attr

# Define the service resource and client globally
dynamodb = boto3.resource('dynamodb')
dynamodb_client = boto3.client('dynamodb')

table = dynamodb.Table('Music')

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

        base_dir = os.path.dirname(__file__)
        abs_file = os.path.join(base_dir, 'a2.json')

        with open(abs_file) as json_file:
            music_data = json.load(json_file, parse_float=Decimal)
        load_music_data(music_data)

    except dynamodb_client.exceptions.ResourceInUseException:
        print("This table already exists")

    #  print(os.path.dirname(__file__))

def get_music_on_query(artist = "", title = "", year = ""):
    """
    :params artist: name of artist to query on
    :type artist: str
    :params title: title of music to query on
    :type artist: str
    :params year: year of music to query on
    :type artist: str
    :returns: list of music based on the query strings
    :rtype: list
    """
    response = {} 
    filter_expression = ''

    if artist and title and year:
        filter_expression = Attr('artist').eq(artist) \
            & Attr('title').eq(title) & Attr('year').eq(year)

    elif artist:
        if title:
            filter_expression = Attr('artist').eq(artist) & Attr('title').eq(title)
        elif year:
            filter_expression = Attr('artist').eq(artist) & Attr('year').eq(year)
        else: 
            filter_expression = Attr('artist').eq(artist)

    elif title:
        if year:
            filter_expression = Attr('artist').eq(artist) & Attr('year').eq(year)

            filter_expression = Attr('title').eq(title)
        else:
            filter_expression = Attr('year').eq(year)


    if filter_expression:
        scan_kwargs = {
            'ProjectionExpression': "title, artist, #yr, img_url",
            'ExpressionAttributeNames': {"#yr": "year"},
            'FilterExpression': filter_expression
        }
        response = table.scan(**scan_kwargs)

    else:
        response = table.scan()

    items = response['Items']

    return items

def load_music_data(music_data):
    for music in music_data['songs']:
        table.put_item(Item=music)

def get_artist_urls():
    scan_kwargs = {
        'ProjectionExpression': 'img_url'
    }

    table = dynamodb.Table('Music')
    response = table.scan(**scan_kwargs)

    artist_img_urls = {item['img_url'] for item in response['Items']}

    return artist_img_urls

def get_music_data(title, artist):
    """
    :params title: title of the music to get
    :type title: str
    :params artist: artist of the music to get
    :type artitst: str
    :returns: dictionary/object containing details about the retrived music
    :rtype: dict

    """
    response = table.get_item(
        Key = {
            'title': title,
            'artist': artist,
        }
    )

    item = response['Item']

    return item
