"""Request Helper."""

from typing import Dict, Text

import aiofiles
import aiohttp
from asyncio_requests.helpers.common.file_helper import download_file_from_s3
from asyncio_requests.helpers.internal.filters_helper import get_ssl_config


async def fetch_file(file_config: Dict):
    """Download file from s3 or from given link or.

    just read from the local pod file path.
    :param file_config: Dict contains s3 config,
    download link, local filepath etc.
    file_config[local_filepath] is mandatory
    """
    if file_config.get('s3_config'):
        await download_file_from_s3(
            file_config['local_filepath'],
            **file_config['s3_config'],
        )
    elif file_config.get('file_download_path'):
        # Add separate aio params when required
        request_type = file_config.get('request_type', 'get')
        async with aiohttp.ClientSession(
                headers=file_config.get('headers')) as session:
            request_obj = getattr(session, request_type.lower())
            session_obj = request_obj(file_config['file_download_path'])
            async with session_obj as response:
                contents = await response.content.read()
                async with aiofiles.open(
                        file_config['local_filepath'], 'wb') as file_obj:
                    await file_obj.write(contents)


async def make_http_request(
        session,
        url: Text,
        filters: Dict,
        request_type: Text,
        **kwargs) -> Dict:
    """Make the API call.

    :param session - Sqlalchemy session object
    :param url - url to hit the api
    :param filters - filters to include in the api
    :param request_type - type of request
    """
    response = kwargs.get('response', {})

    ssl_filters: Dict = await get_ssl_config(
        certificate=kwargs.get('certificate'),
        verify_ssl=kwargs.get('verify_ssl'))
    filters.update(ssl_filters)

    request_obj = getattr(session, request_type.lower())
    session_obj = request_obj(url, **filters)

    async with session_obj as resp:
        response['status_code'] = resp.status
        response['headers'] = dict(resp.headers)
        response['cookies'] = dict(resp.cookies)

        try:
            response['content'] = await resp.content.read()
            # resp.content is a StreamReader
            response['text'] = response['content'].decode()  # convert to str
        except UnicodeDecodeError as err:
            response['error_message'] = \
                f'Error occurred while converting bytes to string - {err}'

    return response
