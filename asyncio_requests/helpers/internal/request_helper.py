"""Request Helper."""

from typing import Dict, Text

import aiofiles
import aiohttp
from asyncio_requests.helpers.common.file_helper import download_file_from_s3
from asyncio_requests.helpers.internal import header_filter_mapping
from asyncio_requests.helpers.internal.filters_helper import get_ssl_config
from asyncio_requests.utils.constants import CHUNK_SIZE_CONSTANT


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


async def file_upload(
        file_name=None,
        file_upload_chunk_size=CHUNK_SIZE_CONSTANT):
    """Generates the chunk of file in a file stream."""
    async with aiofiles.open(file_name, 'rb') as f:
        chunk = await f.read(file_upload_chunk_size)
        while chunk:
            yield chunk
            chunk = await f.read(file_upload_chunk_size)


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
    http_file_download_config = kwargs.get('http_file_download_config')
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

        if http_file_download_config:
            with open(
                http_file_download_config.get('download_filepath'), 'wb'
            )as read_file:
                async for chunk in resp.content.iter_chunked(
                    http_file_download_config.get('file_download_chunk_size')
                ):
                    read_file.write(chunk)
        try:
            response['content'] = await resp.content.read()
            # resp.content is a StreamReader
            response['text'] = response['content'].decode()  # convert to str
        except UnicodeDecodeError as err:
            response['error_message'] = \
                f'Error occurred while converting bytes to string - {err}'

    return response


async def make_http_filters_with_stream_file_upload(
    session,
    url: Text,
    request_type: Text,
    circuit_breaker,
    **kwargs
) -> Dict:
    """Make filters for http call involving file upload in chunks.

    :param session - aiohttp.ClientSession session object
    :param url - url to hit the api
    :param request_type - type of request
    :param circuit_breaker - circuit breaker object.
    """
    http_file_upload_config = kwargs.get('http_file_upload_config')
    local_filepath = http_file_upload_config['local_filepath']
    chunk_size = http_file_upload_config[
        'file_upload_chunk_size']
    filters = {
        'data': file_upload(
            file_name=local_filepath,
            file_upload_chunk_size=chunk_size)
    }
    return await circuit_breaker.failsafe.run(
        make_http_request,
        session,
        url,
        filters,
        request_type,
        **kwargs)


async def make_http_filters_without_stream_uploads(
    session,
    url: Text,
    request_type: Text,
    circuit_breaker,
    **kwargs
) -> Dict:
    """Make filters for file upload over http.

    :param session - aiohttp.ClientSession session object
    :param url - url to hit the api
    :param request_type - type of request
    :param circuit_breaker - circuit breaker object.
    """
    http_file_upload_config = kwargs.get('http_file_upload_config')
    with open(http_file_upload_config['local_filepath'], 'rb') as read_file:
        filters = {
            'data': {
                http_file_upload_config['file_key']: read_file}
        }
        response: Dict = await circuit_breaker.failsafe.run(
            make_http_request,
            session,
            url,
            filters,
            request_type,
            **kwargs)
    return response


async def make_http_filters_without_file(
    session,
    url: Text,
    request_type: Text,
    circuit_breaker,
    **kwargs
) -> Dict:
    """Make filters to make http call.

    :param session - aiohttp.ClientSession session object
    :param url - url to hit the api
    :param request_type - type of request
    :param circuit_breaker - circuit breaker object.
    """
    headers = kwargs.get('headers')
    payload = kwargs.get('payload')
    content_type = headers.get('Content-Type', 'default').lower()
    filters = await header_filter_mapping.get(
        content_type)(
        payload,
        request_type=request_type
    )
    return await circuit_breaker.failsafe.run(
        make_http_request,
        session,
        url,
        filters,
        request_type,
        **kwargs)


filter_methods = {
    'http_with_stream_file_upload': make_http_filters_with_stream_file_upload,
    'http_without_stream_uploads': make_http_filters_without_stream_uploads,
    'http_filters_without_file': make_http_filters_without_file
}


async def handle_http_request(
    session: object,
    url: Text,
    request_type: Text,
    circuit_breaker: object,
    **kwargs
) -> Dict:
    """Identify filter metods to be called before http request.

    :param session - aiohttp.ClientSession session object
    :param url - url to hit the api
    :param request_type - type of request
    :param circuit_breaker - circuit breaker object.
    """
    http_file_upload_config = kwargs.get('http_file_upload_config')
    if http_file_upload_config:
        if http_file_upload_config.get('file_upload_chunk_size'):
            filter_method = filter_methods.get('http_with_stream_file_upload')
        else:
            filter_method = filter_methods.get('http_without_stream_uploads')
    else:
        filter_method = filter_methods.get('http_filters_without_file')

    return await filter_method(
        session,
        url,
        request_type,
        circuit_breaker,
        **kwargs
    )
