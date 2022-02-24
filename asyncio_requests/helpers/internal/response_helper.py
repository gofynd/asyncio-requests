"""Response Helper."""

from typing import Dict, Text

import ujson


async def application_json_response(response: Text) -> Dict:
    """parse_data.

    :param response: Text - Convert this text to dict
    """
    try:
        text = ujson.loads(response)
    except ValueError:
        text = {}

    return text
