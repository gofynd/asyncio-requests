"""Logic."""

from asyncio_requests.logic.http import http_request

protocol_mapping = {
    'HTTP': http_request,
    'HTTPS': http_request,
    'SOAP': None,
    'FTP': None
}
