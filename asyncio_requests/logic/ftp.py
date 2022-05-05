"""Ftp."""

import time
from typing import Dict, Text, Tuple

import aioftp
from asyncio_requests.helpers.internal.circuit_breaker_helper import \
    CircuitBreakerHelper
from asyncio_requests.helpers.internal.filters_helper import get_ssl_config
from asyncio_requests.utils.constants import HTTP_TIMEOUT


async def ftp_request(
        url: Text,
        auth,
        response: Dict,
        info: Dict = None) -> Dict:
    """Aioftp Request.

    :param url: url of ftp server.
    :param auth: auth object aiohttp.BasicAuth(username, password)
        only basicAuth allowed
    :param response: Dict object with following parameters url,
    payload, external_call_request_time, text, error_message
    :param info: protocol_info passed in request function

    url = 'localhost'
    auth = aiohttp.BasicAuth('user','password'),
    protocol = 'FTP'
    protocol_info = {
        'port': 21, # optional ddefault is 21
        'command': 'download', # download, upload, remove
        'server_path': '',
            # path from where to get/delete or upload file on server.
        'client_path': '',
            # path where file is downloaded/uploaded to.
    }
    """
    if info is None:
        info = {}
    start_time = time.time()
    port: int = info.get('port', 21)
    user: Text = auth.login
    password: Text = auth.password
    command_: Text = info.get('command', None)
    server_path: Text = info.get('server_path', None)
    client_path: Text = info.get('client_path', None)
    timeout: int = info.get('timeout', HTTP_TIMEOUT)
    certificate: Tuple[Text] = info.get('certificate', None)
    verify_ssl: bool = info.get('verify_ssl', False)
    if verify_ssl:
        ssl_context: Dict = await get_ssl_config(certificate, verify_ssl)
        verify_ssl = ssl_context.get('ssl_context')
    circuit_breaker_config: Dict = info.get('circuit_breaker_config', {})
    if circuit_breaker_config.get('retry_config'):
        retry_policy_dict: Dict = circuit_breaker_config['retry_config']
        retry_policy = await CircuitBreakerHelper.get_retry_policy(
            **retry_policy_dict)
        circuit_breaker_config['retry_policy'] = retry_policy
    circuit_breaker = CircuitBreakerHelper(**circuit_breaker_config)

    try:
        async with aioftp.Client.context(
            url, port, user, password,
            ssl=verify_ssl,
            connection_timeout=timeout
        ) as client:
            make_ftp_request = getattr(client, command_.lower())
            if client_path:
                await circuit_breaker.failsafe.run(
                    make_ftp_request,
                    server_path,
                    client_path,
                    write_into=True)
            else:
                await circuit_breaker.failsafe.run(
                    make_ftp_request,
                    server_path)
            response['mode'] = command_
            response['file'] = server_path
            response['file_stats'] = await client.stat(server_path)

            return True

    except Exception as request_error:
        response['status_code'] = 999
        response['latency'] = (time.time() - start_time)
        response['text'] = request_error

        return response
