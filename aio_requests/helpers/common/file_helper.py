"""File helper."""

from typing import Text

import aioboto3


async def download_file_from_s3(local_filepath: Text,
                                bucket_name: Text,
                                s3_filepath: Text,
                                access_key: Text,
                                secret_key: Text,
                                region: Text):
    """Download file from AWS S3.

    :param access_key: S3 access key
    :param region: S3 region
    :param secret_key: S3 secret key
    :param bucket_name: bucket name of S3.
    :param s3_filepath: S3 filepath to be downloaded.
    :param local_filepath: local filepath where the file will be saved.
    """
    client = aioboto3.client(
        's3',
        aws_access_key_id=access_key,
        aws_secret_access_key=secret_key,
        region_name=region)
    async with client as s3_client:
        await s3_client.download_file(Bucket=bucket_name,
                                      Key=s3_filepath,
                                      file_save_path=local_filepath)
