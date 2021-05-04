import boto3
from boto3.dynamodb.conditions import Key

from .music import get_music_data

# Define the service resource and client globally
dynamodb = boto3.resource('dynamodb')
dynamodb_client = boto3.client('dynamodb')

table = dynamodb.Table('User_Subscriptions')

def get_subscriptions(username):
    """
    :params username: The username to fetch matching music results on
    :type: str
    :returns: A list containing all music matching on the username
    :rtype: list or None
    """

    response = table.query(
        KeyConditionExpression = Key('username').eq(username)
    )

    items = response['Items']

    if items:
        return items

    return None

def put_subscription(username, title, artist):
    item = get_music_data(artist, title)
    bucket_name = 's3798420-artist-images'
    img_name = item['img_url'].split('/')[-1]

    img = f'https://{bucket_name}.s3.amazonaws.com/{img_name}'

    subscription_item = {
        'username': username,
        'title': item['title'],
        'artist': item['artist'],
        'img': img,
        'year': item['year']
    }

    table.put_item(Item=subscription_item)

def delete_subscription(username, title):
    table.delete_item(
        Key = {
            'username': username,
            'title': title,
        }
    )
