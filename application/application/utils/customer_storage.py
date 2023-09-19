import boto3
from botocore.exceptions import ClientError
from storages.backends.s3boto3 import S3Boto3Storage

from project.settings.environment import aws_settings


class CustomerStorage(S3Boto3Storage):
    pass
