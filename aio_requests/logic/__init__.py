"""Logic."""

from aio_requests.logic.http import http_request

protocol_mapping = {
    'HTTP': http_request,
    'HTTPS': http_request,
    'SOAP': None,
    'FTP': None
}
