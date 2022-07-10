"""Logic."""

from asyncio_requests.logic.ftp import ftp_request
from asyncio_requests.logic.http import http_request
from asyncio_requests.logic.sftp import sftp_request

protocol_mapping = {
    'HTTP': http_request,
    'HTTPS': http_request,
    'SOAP': None,
    'FTP': ftp_request,
    'SFTP': sftp_request
}
