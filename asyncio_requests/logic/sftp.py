"""SFTP."""

import time
from typing import Dict, List, Optional, Text

from asyncio_requests.helpers.internal.circuit_breaker_helper import \
    CircuitBreakerHelper
import asyncssh


async def sftp_request(
        url: Text,
        auth,
        response: Dict,
        info: Dict = None) -> Dict:
    """sftp."""
    if info is None:
        info = {}
    start_time = time.time()
    port: int = info.get('port', 22)
    user: Text = auth.login
    password: Text = auth.password
    mode_: Text = info.get('mode', None)
    remote_path: Text = info.get('remote_path', None)
    local_path: Text = info.get('local_path', None)
    remote_files: Optional[List, Text] = remote_path
    additional_arguments: Dict = info.get('additional_arguments', {})

    circuit_breaker_config: Dict = info.get('circuit_breaker_config', {})
    if circuit_breaker_config.get('retry_config'):
        retry_policy_dict: Dict = circuit_breaker_config['retry_config']
        retry_policy = await CircuitBreakerHelper.get_retry_policy(
            **retry_policy_dict)
        circuit_breaker_config['retry_policy'] = retry_policy
    circuit_breaker = CircuitBreakerHelper(**circuit_breaker_config)

    try:
        async with asyncssh.connect(host=url,
                                    username=user,
                                    password=password,
                                    port=port,
                                    known_hosts=None) as conn:
            async with conn.start_sftp_client() as sftp:
                lstat = {
                    i.split(':')[0]: i.split(':')[1]
                    for i in str(await sftp.lstat(remote_path)).split(',')
                    }
                # getting files list for directory
                print(lstat)
                if 'directory' in lstat['type']:
                    remote_files: List = await sftp.listdir(remote_path)
                    additional_arguments.update({'recurse': True})

                make_sftp_request = getattr(sftp, mode_.lower())
                if local_path:
                    await circuit_breaker.failsafe.run(
                        make_sftp_request,
                        remote_path,
                        local_path,
                        **additional_arguments)
                else:
                    await circuit_breaker.failsafe.run(
                        make_sftp_request,
                        remote_path,
                        **additional_arguments)

                response['mode'] = mode_
                response['file_stats'] = lstat
                response['files'] = remote_files
                response['tat'] = (time.time() - start_time)
            return True

    except Exception as request_error:
        response['status_code'] = 999
        response['latency'] = (time.time() - start_time)
        response['text'] = request_error

        return response
