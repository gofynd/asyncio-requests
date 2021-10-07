from aio_requests.helpers.common.date_helper import get_ist_now
from aio_requests.logic import protocol_mapping


async def request(
        url,
        data,
        auth=None,
        protocol="",
        protocol_info=None
):
    common_response = {
        "url": url,
        "payload": data,
        "external_call_request_time": str(get_ist_now()),
        "text": "",
        "error_message": "",
    }

    if not protocol_mapping.get(protocol.upper()):
        common_response["error_message"] = "No Protocol Specified"
        return common_response

    response = await protocol_mapping[protocol](url, data, auth, common_response, info=protocol_info)
    return response
