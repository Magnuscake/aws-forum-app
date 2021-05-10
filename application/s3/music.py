import requests
import logging

import boto3
from botocore.exceptions import ClientError

s3 = boto3.resource('s3')
s3_client = boto3.client('s3')

BUCKET_NAME = 's3798420-artist-images'

def upload_artist_images(artist_img_urls):
    """Upload images of the artists from a list of urls
    :params artist_img_urls: List containing all the artist images
    :type artist_img_urls: list
    :returns: None
    """
    for url in artist_img_urls:
        # To check if the image already exists in the bucket
        key = url.split('/')[-1]

        if not key_exists_in_bucket(key):
            upload_image_from_url(url)

def upload_image_from_url(url):
    """Upload image to the s3 bucket with a key based on the ending string of the url
    :params url: Url of the image to upload
    :type url: str
    :returns: None
    """

    r = requests.get(url, stream = True)

    key = url.split('/')[-1]

    bucket = s3.Bucket(BUCKET_NAME)
    bucket.upload_fileobj(r.raw, key)

def key_exists_in_bucket(key):
    """Check if the given key exists in the bucket
    :params key: Key (name) of the image to check on
    :type key: string
    :returns: True if the key exists, else False
    :rtype: Bool
    """

    try:
        s3.Object(BUCKET_NAME, key).load()

    except ClientError:
        return False

    return True
