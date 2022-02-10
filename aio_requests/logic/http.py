import aiohttp
import aiofiles
import aiofiles.os
import time
import ujson

from aio_requests.utils.request_tracer import request_tracer
from aio_requests.utils.constants import HTTP_TIMEOUT

from aio_requests.helpers.internal import header_filter_mapping
from aio_requests.helpers.internal import header_response_mapping

from aio_requests.helpers.internal.request_helper import make_http_request, fetch_file
from aio_requests.helpers.internal.circuit_breaker_helper import CircuitBreakerHelper


async def http_request(url, auth, response, info=None):
    if info is None:
        info = {}
    start_time = time.time()
    timeout = info.get("timeout", HTTP_TIMEOUT)
    request_type = info["request_type"]
    certificate = info.get("certificate")
    verify_ssl = info.get("verify_ssl", True)
    cookies = info.get("cookies")
    headers = info.get("headers", {})
    trace_config = info.get("trace_config", [request_tracer()])
    http_file_config = info.get("http_file_config", {})
    serialization = info.get("serialization", ujson.dumps)
    circuit_breaker_config = info.get("circuit_breaker_config", {})

    timeout = aiohttp.ClientTimeout(total=timeout)
    if circuit_breaker_config.get("retry_config"):
        retry_policy_dict = circuit_breaker_config["retry_config"]
        retry_policy = await CircuitBreakerHelper.get_retry_policy(**retry_policy_dict)
        circuit_breaker_config["retry_policy"] = retry_policy
    circuit_breaker = CircuitBreakerHelper(**circuit_breaker_config)

    async with aiohttp.ClientSession(
            trace_configs=trace_config, cookies=cookies, headers=headers,
            timeout=timeout, auth=auth, json_serialize=serialization
    ) as session:
        try:
            if http_file_config:
                await fetch_file(http_file_config)
                with open(http_file_config["local_filepath"], "rb") as read_file:  # aiohttp doesnt support
                    filters = {"data": {http_file_config["file_key"]: read_file}}
                    response = await circuit_breaker.failsafe.run(make_http_request, session, url, filters,
                                                                  request_type, certificate=certificate,
                                                                  verify_ssl=verify_ssl)
            else:
                content_type = headers.get("Content-Type", "default").lower()
                filters = await header_filter_mapping.get(content_type)(response["payload"], request_type=request_type)
                response = await circuit_breaker.failsafe.run(make_http_request, session, url, filters, request_type,
                                                              certificate=certificate, verify_ssl=verify_ssl)
            res_content_type = response["headers"].get("Content-Type", "default").lower()
            response["json"] = await header_response_mapping.get(res_content_type)(response["text"]) if \
                header_response_mapping.get(res_content_type) else ""
        except Exception as request_error:
            response["status_code"] = 999
            response["latency"] = (time.time() - start_time)
            response["text"] = request_error

        return response
