"""Aio request."""

from typing import Dict, Optional, Text, Union

from asyncio_requests.helpers.common.date_helper import get_ist_now
from asyncio_requests.logic import protocol_mapping


async def request(
        url: Text,
        data: Optional[Union[Dict, Text]] = None,
        auth: object = None,
        protocol: Text = '',
        protocol_info: Dict = None,
        pre_processor_config: Dict = None,
        post_processor_config: Dict = None,
        **kwargs
) -> Dict:
    """Multiple protocols.

     calls with pre-processor, post processor and retry support.
    :param url: URL to call
    :param data: Data to be sent in calls
    :param protocol: values HTTP/HTTPS
    :param auth: aiohttp.BasicAuth(username, password)
        Optional field any auth abject is accepted supported by aiohttp
    :param protocol_info: {
        "request_type": "GET", #required
        "timeout": int, #Optional
        "certificate: "", #Optional,
        "verify_ssl": Boolean, #Optional,
        "cookies": "", #Optional,
        "headers": {}, #Optional,
        "trace_config": request tracer object list,
            #Optional default is [aiohttp.TraceConfig()]
        "http_file_upload_config" {
            "local_filepath": "required",
            "file_key": "required",
            "delete_local_file": "boolean Optional"
        }, #optional,
        "serialization": ujson.dumps, #Optional
        "circuit_breaker_config": {
            "maximum_failures": "int optional",
            "timeout": "int optional",
            "retry_config": {
                "name": "str required",
                "allowed_retries": "int required",
                "retriable_exceptions": [Optional list of Exceptions],
                list of exception types indicating which
                    exceptions can cause a retry.
                    If None every exception is considered retriable
                "abortable_exceptions": [Optional list of Exceptions],
                    list of exception types indicating which
                    exceptions should abort failsafe run
                    immediately and be propagated out of failsafe. If None, no
                    exception is considered abortable.
                "on_retries_exhausted": Optional callable
                    that will be invoked on a retries exhausted event,
                "on_failed_attempt": Optional callable that
                    will be invoked on a failed attempt event,
                "on_abort": Optional callable that will be
                    invoked on an abort event,
                "delay": int seconds of delay between
                    retries Optional default 0,
                "max_delay": int seconds of max delay between
                    retries Optional default 0,
                "jitter": Boolean Optional, False when you want to
                    keep the wait between calls constant else True
            } #Optional Include this if you want retry
        } #Optional
    }
    :param pre_processor_config: Expects Dict {
        "function": function_address, #required
        "params": {
            "param1": value1
        } #optional
    } Optional
    :param post_processor_config: Expects Dict
    {"function": function_address, "params": {"param1": value1}} Optional
    """
    if data is None:
        data = {}

    response: Dict = {
        'url': url,
        'payload': data,
        'external_call_request_time': str(get_ist_now()),
        'text': '',
        'error_message': '',
    }

    if not protocol_mapping.get(protocol.upper()):
        response['error_message'] = 'No Protocol Specified'
        return response

    if pre_processor_config:
        response['pre_processor_response']: Dict = await \
            pre_processor_config['function'](response=response,
                                             **pre_processor_config.get(
                                                 'params',
                                                 {}))

    response['api_response']: Dict = await \
        protocol_mapping[protocol](url, auth, response, info=protocol_info)

    if post_processor_config:
        response['post_processor_response']: Dict = \
            await post_processor_config['function'](
                response=response,
                **post_processor_config.get(
                    'params', {}))
    return response
