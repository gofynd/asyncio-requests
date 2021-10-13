import ujson


async def application_json_response(response):
    """parse_data."""
    try:
        text = ujson.loads(response)
    except ValueError:
        text = {}

    return text