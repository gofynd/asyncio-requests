"""Filters Helper."""

import aiohttp

import ssl
from typing import Dict, Optional, Text, Tuple, Union

import ujson


async def get_ssl_config(
        certificate: Tuple[Text] = None,
        verify_ssl: bool = None) -> Dict:
    """Get the SSL config.

    :param certificate: Tuple[Text] - ('certificate path',
        'certificate key path')
    :param verify_ssl: bool - Flag to enable ssl verification
    """
    # verify_ssl, ssl_context, fingerprint and ssl parameters
    # are mutually exclusive
    # Some don't use ssl; but use an IP whereas some use
    # SSL Certificate and those combined
    # usage in aiohttp session_obj contradict each other
    # thereby raising a ValueError Exception
    if certificate:
        ssl_context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
        ssl_context.load_cert_chain(certificate[0], certificate[1])
        return {
            'ssl_context': ssl_context
        }
    return {
        'ssl': verify_ssl or True
    }


async def form_x_www_form_urlencoded_filters(data: Dict, **kwargs) -> Dict:
    """Make filters for the API to be hit if the header.

    is application/x-www-form-urlencoded
    :param data: Dict - data to be hit in the API.
    """
    form_data = aiohttp.FormData()
    for form_key, form_value in data.items():
        value = ujson.dumps(form_value) if \
            isinstance(form_value, dict) else form_value
        form_data.add_field(form_key, value)
    filters = {'data': form_data}
    return filters


async def application_json_filters(
        data: Optional[Union[Dict, Text]], **kwargs) -> Dict:
    """Make filters for the API to be hit if the header is application/json.

    :param data: Dict or Text - data to be hit in the API.
    """
    filters = {}
    request_type: Text = kwargs['request_type']
    http_file_upload_config: Dict = kwargs.get('http_file_upload_config')
    if request_type == 'GET':
        if http_file_upload_config:
            pass
        else:
            if isinstance(data, dict):
                data.update(
                    {
                        key: str(data[key]) for
                        key in data if type(data[key]) in [bool]
                    }
                )
                filters = {'params': data}
    else:
        if isinstance(data, dict):
            filters = {'json': data}
        else:
            if not isinstance(data, str):
                data = ujson.dumps(data)
            filters = {'data': data}
    return filters
