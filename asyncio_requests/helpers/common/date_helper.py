"""Date helper."""
from asyncio_requests.utils.constants import TIMEZONE

from datetime import datetime

import pytz


timezone = pytz.timezone(TIMEZONE)


def get_ist_now(timezone=timezone) -> datetime:
    """Returns Indian Standard Time datetime object.

    Returns:
        object -- Datetime object
    """
    return datetime.now(timezone)
