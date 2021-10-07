import aiohttp
import ssl
import ujson


async def get_ssl_config(certificate=None, verify_ssl=None):
    # verify_ssl, ssl_context, fingerprint and ssl parameters are mutually exclusive
    # Some doesnt use ssl; but use an IP whereas some use SSL Certificate and those combined
    # usage in aiohttp session_obj contradict each other thereby raising a ValueError Exception
    if certificate:
        ssl_context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
        ssl_context.load_cert_chain(certificate[0], certificate[1])
        return {
            "ssl_context": ssl_context
        }
    return {
        "ssl": verify_ssl or True
    }


async def form_x_www_form_urlencoded_filters(data, **kwargs):
    form_data = aiohttp.FormData()
    for form_key, form_value in data.items():
        value = ujson.dumps(form_value) if isinstance(form_value, dict) else form_value
        form_data.add_field(form_key, value)
    filters = {"data": form_data}
    return filters


async def form_application_json_filters(data, **kwargs):
    filters = {}
    request_type = kwargs["request_type"]
    http_file_config = kwargs.get("http_file_config")
    if request_type == "GET":
        if http_file_config:
            pass
        else:
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
    return filters
