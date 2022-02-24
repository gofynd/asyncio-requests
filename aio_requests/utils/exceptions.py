"""Exceptions."""

from typing import Dict, Optional, Text


class CustomGlobalException(Exception):
    """Class CustomGlobalException."""

    def __init__(self,
                 headline: Text,
                 error_code: int,
                 error_msg: Optional[Text] = '',
                 error_data: Optional[Dict] = None):
        """Custom exception with headline."""
        self.headline = headline
        self.error_code = error_code
        self.error_msg: Optional[Text] = error_msg
        self.error_data = error_data or {}

    def __str__(self) -> Text:
        """Return appropriate error exception str."""
        return f'{self.headline} | ' \
               f'{self.error_code} | ' \
               f'{self.error_msg} | ' \
               f'{self.error_data}'
