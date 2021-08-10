import aiohttp
import ujson
from aio_requests.utils.request_tracer import request_tracer
from aio_requests.utils.data_helper import parse_data
from aio_requests.utils.date_helper import get_ist_now


async def http_request(cert, ssl, timeout_allowed, auth, url, request_type, data, cookies, headers, verify_ssl, response):
    timeout = aiohttp.ClientTimeout(total=timeout_allowed)
    auth = aiohttp.BasicAuth(auth["username"], auth["password"]) if auth else None
    ssl_context = None

    if cert:
        ssl_context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
        ssl_context.load_cert_chain(cert[0], cert[1])

    async with aiohttp.ClientSession(
            trace_configs=[request_tracer()], cookies=cookies, headers=headers,
            timeout=timeout, auth=auth, json_serialize=ujson.dumps
    ) as session:

        # verify_ssl, ssl_context, fingerprint and ssl parameters are mutually exclusive
        # Jiopos doesnt use ssl; it uses an IP in production whereas Amazon uses SSL Certificate and those combined
        # usage in aiohttp session_obj contradict each other thereby raising a ValueError Exception

        filters = {}
        if data and headers.get("Content-Type") == "application/x-www-form-urlencoded":
            form_data = aiohttp.FormData()
            for form_key, form_value in data.items():
                value = ujson.dumps(form_value) if isinstance(form_value, dict) else form_value
                form_data.add_field(form_key, value)
            filters = {"data": form_data}
        else:
            if request_type == "GET":
                if isinstance(data, dict):
                    data.update(
                        {
                            key: str(data[key]) for key in data if type(data[key]) in [bool]
                        }
                    )
                    filters = {"params": data}
            else:
                if isinstance(data, dict):
                    filters = {"json": data}
                else:
                    if not isinstance(data, str):
                        data = ujson.dumps(data)
                    filters = {"data": data}

        if ssl_context:
            filters.update({"ssl_context": ssl_context})
        else:
            filters.update({"ssl": verify_ssl})

        request_obj = getattr(session, request_type.lower())
        session_obj = request_obj(url, **filters)

        async with session_obj as resp:
            response["status_code"] = resp.status
            response["headers"] = dict(resp.headers)
            response["cookies"] = dict(resp.cookies)

            try:
                response["content"] = await resp.content.read()  # resp.content is a StreamReader
                response["text"] = response["content"].decode()  # converting to str
            except UnicodeDecodeError as err:
                response["error_message"] = f"Error occurred while converting bytes to string - {err}"

        response["json"] = parse_data(response["text"])

        return response