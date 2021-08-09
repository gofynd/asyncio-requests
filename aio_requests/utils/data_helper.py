def parse_data(data):
    """parse_data."""
    try:
        text = ujson.loads(data)

    except ValueError:
        text = {}

    return text
