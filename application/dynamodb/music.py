import json
import os
from decimal import Decimal

import boto3
from boto3.dynamodb.conditions import Attr

# Define the service resource and client globally
dynamodb = boto3.resource('dynamodb')
dynamodb_client = boto3.client('dynamodb')

TABLE_NAME = "Music"
table = dynamodb.Table(TABLE_NAME)

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

    except dynamodb_client.exceptions.ResourceInUseException:
        print(f"Table {TABLE_NAME} already exists")

    # Then load the music data
    # Also loads any missing or deleted data
    base_dir = os.path.dirname(__file__)
    abs_file = os.path.join(base_dir, 'a2.json')

    with open(abs_file) as json_file:
        music_data = json.load(json_file, parse_float=Decimal)

    load_music_data(music_data)


def get_music_on_query(artist = "", title = "", year = ""):
    """
    :params artist: Name of artist to query on
    :type artist: str
    :params title: Title of music to query on
    :type artist: str
    :params year: Year of music to query on
    :type artist: str
    :returns: List of music based on the query strings
    :rtype: list
    """
    response = {} 
    filter_expression = ''

    if artist or title or year:
        if artist and title and year:
            filter_expression = Attr('artist').eq(artist) \
                & Attr('title').eq(title) & Attr('year').eq(year)

        # Set the filter expression query according to the available fields
        elif artist:
            if title:
                filter_expression = Attr('artist').eq(artist) & Attr('title').eq(title)
            elif year:
                filter_expression = Attr('artist').eq(artist) & Attr('year').eq(year)
            else: 
                filter_expression = Attr('artist').eq(artist)

        elif title:
            if year:
                filter_expression = Attr('title').eq(title) & Attr('year').eq(year)

                filter_expression = Attr('title').eq(title)
        else:
            filter_expression = Attr('year').eq(year)

        scan_kwargs = {
            'ProjectionExpression': "title, artist, #yr, img_url",
            'ExpressionAttributeNames': {"#yr": "year"},
            'FilterExpression': filter_expression
        }
        response = table.scan(**scan_kwargs)

    else:
        response = table.scan()

    items = response['Items']

    for item in items:
        img_name = item['img_url'].split('/')[-1]
        s3_url = f"https://s3798420-artist-images.s3.amazonaws.com/{img_name}"
        
        item['img_url'] = s3_url

    return items


def load_music_data(music_data):
    """Loads data into music table
    
    :params music_data: json file to load the music data from
    "returns: None
    """

    for music in music_data['songs']:
        music_artist = music['artist']
        music_title = music['title']

        item = get_music_data(music_artist, music_title)

        # Only put data that is not in the table
        if not item:
            table.put_item(Item=music)


def get_artist_urls():
    try:
        scan_kwargs = {
            'ProjectionExpression': 'img_url'
        }

        response = table.scan(**scan_kwargs)

        artist_img_urls = {item['img_url'] for item in response['Items']}

        return artist_img_urls

    except dynamodb_client.exceptions.ResourceNotFoundException:
        print("The table you are trying to scan does not exist")

    return []


def get_music_data(artist, title):
    """Fetch music from the music table on the provided Keys
    :params title: title of the music to fetch
    :type title: str
    :params artist: artist of the music to fetch
    :type artitst: str
    :returns: dictionary/object containing details about the retrived music
    :rtype: dict
    """

    try:
        response = table.get_item(
            Key = {
                'title': title,
                'artist': artist,
            }
        )

        return response['Item']
    except KeyError: 
        return {}
