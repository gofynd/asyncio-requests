from aio_requests.helpers.internal.filters_helper import form_x_www_form_urlencoded_filters, form_application_json_filters


header_mapping = {
    "application/x-www-form-urlencoded": form_x_www_form_urlencoded_filters,
    "application/json": form_application_json_filters,
    "default": form_application_json_filters
}  # ToDo Add multipart header

