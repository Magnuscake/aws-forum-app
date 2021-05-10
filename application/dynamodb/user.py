import os
import json
from decimal import Decimal

import boto3
from boto3.dynamodb.conditions import Key, Attr

# Define the service resource and client globally
dynamodb = boto3.resource('dynamodb')
dynamodb_client = boto3.client('dynamodb')

TABLE_NAME = "User_Details"
table = dynamodb.Table(TABLE_NAME)

def put_user(email, username, password):
    """Insert an user item into the user table
    :params email: Email of the new user
    :type email: str
    :params username: username of the new user
    :type username: str
    :params password: password of the new user
    :type password: str
    :returns: The response object
    :rtype: dict
    """

    response = table.put_item(
        Item = {
            'email': email,
            'username': username,
            'password': password
        }
    )

    return response

def key_exists(key, value):
    """Check if the given key value pair exists in the database table. This is
        mainly used to check for primary key value, specifically the Hash key and
        Range Key
    :params key: Key of the property to check on
    :type key: str
    :params value: Value of the property to check on
    :type key: str
    :returns: True if an item with the given key value pair exists, else False
    :rtype: Bool
    """

    response = table.query(
        KeyConditionExpression = Key(key).eq(value)
    )

    if response['Items']:
        return True

    return False

def attr_exists(attribute, user_input):
    """Check if the given key value pair exists in the database table. This is
        used to check for non key attributes
    :params attribute: Attribute of the property to check on
    :type attribute: str
    :params user_input: Value based on the user input to check on
    :type user_input: str
    :returns: True if an item with the given key value pair exists, else False
    :rtype: Bool
    """

    response = table.scan(
        FilterExpression = Attr(attribute).eq(user_input)
    )

    if response['Items']:
        return True

    return False

def login_user(email, password):
    """This is the main function that logs in a user. Based on the given email
        and password, if an item with the given email exists, the function checks
        if the password in that item is the same password that is passed to the
        function. If everything checks out, it returns a dict containing all the
        user info
    :params email: Email of the user trying to log in
    :type email: str
    :params password: Password of the user trying to log in
    :type password: str
    :returns: dict containing user info if user exists, else an empty dict
    :rtype: dict
    """

    response = table.get_item(
        Key={
            'email': email
        }
    )

    item = response['Item']

    if not item['password'] == password:
        return {}

    return item

def load_users():
    """Load users into the dynamodb table from the given json file
    :returns: None
    """
    try:
        # json file should be in the same file location as the function
        base_dir = os.path.dirname(__file__)
        abs_file = os.path.join(base_dir, 'users.json')

        with open(abs_file) as json_file:
            users = json.load(json_file, parse_float=Decimal)

            for user in users['users']:
                #  Check if the user already exists in the table
                response = key_exists('email', user['email'])

                if not response:
                    table.put_item(Item=user)

    except dynamodb_client.exceptions.ResourceNotFoundException:
        print("The table you are trying to query does not exist")

