"""Http."""

import time
from typing import Any, Callable, Dict, List, Text, Tuple

import aiohttp
from asyncio_requests.helpers.internal import header_response_mapping
from asyncio_requests.helpers.internal.circuit_breaker_helper import \
    CircuitBreakerHelper
from asyncio_requests.helpers.internal.request_helper import \
    handle_http_request
from asyncio_requests.utils.constants import HTTP_TIMEOUT
from asyncio_requests.utils.request_tracer import request_tracer
import ujson


async def http_request(
        url: Text,
        auth,
        response: Dict,
        info: Dict = None) -> Dict:
    """Aiohttp Request.

    :param url: url to make http call.
    :param auth: auth object for ex aiohttp.BasicAuth(username, password)
    :param response: Dict object with following parameters url,
    payload, external_call_request_time, text, error_message
    :param info: protocol_info passed in request function
    """
    if info is None:
        info = {}
    start_time = time.time()
    timeout: int = info.get('timeout', HTTP_TIMEOUT)
    request_type: Text = info['request_type']
    certificate: Tuple[Text] = info.get('certificate')
    verify_ssl: bool = info.get('verify_ssl', True)
    cookies: Any = info.get('cookies')
    headers: Dict = info.get('headers', {})
    trace_config: List[aiohttp.TraceConfig()] = info.get(
        'trace_config', [request_tracer()])
    http_file_upload_config: Dict = info.get('http_file_upload_config', {})
    file_download_config: Dict = info.get('http_file_download_config', {})
    serialization: Callable = info.get('serialization', ujson.dumps)
    circuit_breaker_config: Dict = info.get('circuit_breaker_config', {})

    timeout: aiohttp.ClientTimeout = aiohttp.ClientTimeout(total=timeout)
    if circuit_breaker_config.get('retry_config'):
        retry_policy_dict: Dict = circuit_breaker_config['retry_config']
        retry_policy = await CircuitBreakerHelper.get_retry_policy(
            **retry_policy_dict)
        circuit_breaker_config['retry_policy'] = retry_policy
    circuit_breaker = CircuitBreakerHelper(**circuit_breaker_config)

    async with aiohttp.ClientSession(
            trace_configs=trace_config, cookies=cookies, headers=headers,
            timeout=timeout, auth=auth, json_serialize=serialization
    ) as session:
        try:
            response = await handle_http_request(
                session,
                url,
                request_type,
                circuit_breaker,
                headers=headers,
                payload=response['payload'],
                certificate=certificate,
                verify_ssl=verify_ssl,
                http_file_download_config=file_download_config,
                http_file_upload_config=http_file_upload_config,
            )
            res_content_type: Text = response['headers'].get(
                'Content-Type', 'default').lower()
            response['json'] = ''
            for content_type_value in header_response_mapping.keys():
                if content_type_value in res_content_type:
                    response['json'] = await header_response_mapping[
                        content_type_value](response['text'])
            response['request_tracer'] = [
                tc.results_collector for tc in trace_config
            ]
            response['latency'] = (time.time() - start_time)
        except Exception as request_error:
            response['status_code'] = 999
            response['latency'] = (time.time() - start_time)
            response['text'] = request_error

        return response
