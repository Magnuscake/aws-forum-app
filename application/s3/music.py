import requests
import logging

import boto3
from botocore.exceptions import ClientError

s3 = boto3.resource('s3')
s3_client = boto3.client('s3')

def create_bucket(bucket_name, region=None):

    """Create an S3 bucket in a specified region

    If a region is not specified, the bucket is created in the S3 default

    region (us-east-1).

    :param bucket_name: Bucket to create
    :param region: String region to create bucket in, e.g., 'us-west-2'
    :return: True if bucket created, else False

    """

    try:
        if region is None:
            s3_client = boto3.client('s3')
            s3_client.create_bucket(Bucket=bucket_name)

        else:
            s3_client = boto3.client('s3', region_name=region)

            location = {'LocationConstraint': region}

            s3_client.create_bucket(Bucket=bucket_name, 
                                    CreateBucketConfiguration=location)

    except ClientError as e:

        logging.error(e)

        return False

    return True 

def upload_artist_images(artist_img_urls):
    bucket_name = 's3798420-artist-images'

    for item in artist_img_urls:
        key = item.split('/')[-1]
        if key_exists_in_bucket(bucket_name, key):
            continue
    
        upload_image_from_url(bucket_name, item)

def upload_image_from_url(bucket_name, url):
    r = requests.get(url, stream = True)

    key = url.split('/')[-1]

    bucket = s3.Bucket(bucket_name)
    bucket.upload_fileobj(r.raw, key)

def key_exists_in_bucket(bucket_name, key):
    try:
        s3.Object(bucket_name, key).load()

    except ClientError as e:
        logging.error(e)
        return False

    return True
