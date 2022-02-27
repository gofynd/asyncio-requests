"""Internal."""

from asyncio_requests.helpers.internal.filters_helper import \
    application_json_filters, form_x_www_form_urlencoded_filters
from asyncio_requests.helpers.internal.response_helper import \
    application_json_response

header_filter_mapping = {
    'application/x-www-form-urlencoded': form_x_www_form_urlencoded_filters,
    'application/json': application_json_filters,
    'default': application_json_filters
}  # ToDo Add multipart header

header_response_mapping = {
    'application/json': application_json_response,
    'default': application_json_response
}
