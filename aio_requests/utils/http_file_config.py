"""Http file config utils."""

import os
from typing import Text

import aioboto3
import aiofiles
import aiohttp

from .constants import STATUS_CODE_403
from .exceptions import CustomGlobalException


async def download_file_from_s3(bucket_name: Text,
                                s3_filepath: Text,
                                local_filepath: Text,
                                access_key: Text = None,
                                secret_key: Text = None,
                                region: Text = None, **kwargs):
    """Download file from AWS S3.

    :param access_key: S3 access key
    :param region: S3 region
    :param secret_key: S3 secret key
    :param bucket_name: bucket name of S3.
    :param s3_filepath: S3 filepath to be downloaded.
    :param local_filepath: local filepath where the file will be saved.
    :param kwargs
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


async def download_file_from_url(
        file_download_path: Text,
        local_filepath: Text,
        request_type: Text = 'get',
        headers=None, **kwargs):
    """Download File from url.

    :param file_download_path: complete url from where to download
    :param local_filepath: machine file path to download and store it
    :param request_type: HTTP method
    :param headers: API headers if any
    :param kwargs
    """
    if headers is None:
        headers = {}
    async with aiohttp.ClientSession(headers=headers) as session:
        request_obj = getattr(session, request_type.lower())
        session_obj = request_obj(file_download_path)
        async with session_obj as response:
            contents = await response.content.read()
            if response.status == STATUS_CODE_403:
                raise CustomGlobalException(
                    contents, STATUS_CODE_403,
                    error_data={
                        'error_message':
                            'Access to the requested file is forbidden.'
                    })
            async with aiofiles.open(local_filepath, 'wb') as file_obj:
                await file_obj.write(contents)


async def delete_local_file_path(local_filepath: Text, **kwargs):
    """Deletes downloaded file.

    :param local_filepath: file to be deleted
    :param kwargs
    """
    os.remove(local_filepath)
