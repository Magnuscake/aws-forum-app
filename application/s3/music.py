import requests
import logging

import boto3
from botocore.exceptions import ClientError

s3 = boto3.resource('s3')
s3_client = boto3.client('s3')

BUCKET_NAME = 's3798420-artist-images'

def upload_artist_images(artist_img_urls):

    for url in artist_img_urls:
        key = url.split('/')[-1]
        if not key_exists_in_bucket(key):
            upload_image_from_url(url)

def upload_image_from_url(url):
    r = requests.get(url, stream = True)

    key = url.split('/')[-1]

    bucket = s3.Bucket(BUCKET_NAME)
    bucket.upload_fileobj(r.raw, key)

def key_exists_in_bucket(key):
    try:
        s3.Object(BUCKET_NAME, key).load()

    except ClientError as ce:
        logging.error(ce)
        return False

    return True
