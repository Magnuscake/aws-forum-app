import boto3
from boto3.dynamodb.conditions import Key

from .music import get_music_data

# Define the service resource and client globally
dynamodb = boto3.resource('dynamodb')
dynamodb_client = boto3.client('dynamodb')

table = dynamodb.Table('User_Subscriptions')

def get_subscriptions(username):
    """Fetch a list of subscriptions from the subscriptions table based on the given key (username)
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
    """Insert an item into the subscriptions table
    :paramas username: Username of user who subscribed to the music
    "type username: str
    :params title: Title of music the user subscribed to
    :type title: str
    :params artist: Artist of the music the user subscribed to
    :type artist: str
    :returns: None
    """

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
    """Delete an item from the subscriptions table
    :params username: username (Key) of the user
    :type username: str
    :params title: title (Key) of the music
    :type title: str
    :returns: None
    """

    table.delete_item(
        Key = {
            'username': username,
            'title': title,
        }
    )
