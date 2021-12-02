from aio_requests.helpers.common.date_helper import get_ist_now
from aio_requests.logic import protocol_mapping


async def request(
        url,
        data,
        auth=None,
        protocol="",
        protocol_info=None,
        pre_processor=None,
        post_processor=None
):
    response = {
        "url": url,
        "payload": data,
        "external_call_request_time": str(get_ist_now()),
        "text": "",
        "error_message": "",
    }

    if not protocol_mapping.get(protocol.upper()):
        response["error_message"] = "No Protocol Specified"
        return response

    if pre_processor:
        response["pre_processor_response"] = await pre_processor(url, data, auth, protocol, response, info=protocol_info)

    processor_response = await protocol_mapping[protocol](url, data, auth, response, info=protocol_info)
    response.update(processor_response)

    if post_processor:
        response["post_processor_response"] = await post_processor(url, data, auth, response, info=protocol_info)

    return response
