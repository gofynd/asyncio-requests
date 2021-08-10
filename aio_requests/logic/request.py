from aio_requests.logic.http import http_request
from aio_requests.logic.soap import soap_request
from aio_requests.utils.constants import HTTP_TIMEOUT
from aio_requests.utils.date_helper import get_ist_now
from time import time
import ssl


async def request(
        request_type,
        url,
        data=None,
        headers=None,
        auth=None,
        cookies=None,
        cert=None,
        verify_ssl=True,
        protocol="HTTP",
        timeout_allowed=HTTP_TIMEOUT,
):
    """Asynchronous HTTP Request Method.

    :param protocol: HTTP or HTTPS
    :param verify_ssl: This param is used for a request ignoring ssl verification (Too Risky) (Used in Jiopos)
    :param cert: certificate path as tuple (used in amazon)
    :param cookies:
    :param auth:
    :param request_type: String GET/POST/PUT
    :param url: String
    :param data: Dict  Nullable
    :param headers: Dict Nullable
    :param timeout_allowed: int Max timeout allowed for API call
    :return: Tuple with status_code and json response


    Example:
    resp1 = await aiohttp_request('GET', 'http://localhost:8000/ping/', data={'a': 1})
    print(resp1)

    resp2 = await aiohttp_request('POST', 'http://localhost:8000/pong/', data={'a': 1})
    print(resp2)

    """
    if auth is None:
        auth = {}
    if headers is None:
        headers = {}
    start_time = time()

    response = {
        "url": url,
        "method": request_type,
        "payload": data,
        "external_call_request_time": str(get_ist_now()),
        "status_code": None,
        "text": "",
        "headers": "",
        "cookies": None,
        "error_message": "",
    }
    try:
        if protocol == "HTTP":
            response = await http_request(cert, ssl, timeout_allowed, auth, url, request_type, data, cookies, headers, verify_ssl, response)
        elif protocol == "SOAP":
            response = await soap_request(url=url, data=data, auth=auth, response=response, timeout=timeout_allowed)
        else:
            raise Exception("Invalid request_type: {}".format(request_type))
        response["latency"] = time() - start_time

    except Exception as request_error:
        response["status_code"] = 999
        response["latency"] = (time() - start_time)
        response["text"] = request_error

        return response
