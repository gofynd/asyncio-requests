from logic_test import logic_test
from aio_requests.aio_request import request
import asyncio


async def test(*args, **kwargs):
    return {"text": "final res"}


# https://api.fyndx1.de/masquerader/v1/aio-request-test/get
# https://api.fyndx1.de/masquerader/v1/aio-request-test/post
# https://api.fyndx1.de/masquerader/v1/aio-request-test/put
# https://api.fyndx1.de/masquerader/v1/aio-request-test/delete
# http://116.50.64.106:8080/fynd/orders/S127163135/invoice/b2b/file


res = asyncio.run(
    request(
        url="http://116.50.64.106:8080/fynd/orders/S127163135/invoice/b2b/file",
        data={
            "key0": "val0"
        },
        protocol="HTTP",
        protocol_info={
            "request_type": "POST",
            "circuit_breaker_config": {
                "timeout": 150,
                "retry_config": {
                    "name": "asdf",
                    "allowed_retries": 1
                }
            },
            "http_file_config": {
                "local_filepath": "/tmp/temp.pdf",
                "file_key": "file"
            }
        },
        # pre_processor_config={
        #     "function": request,
        #     "async_enabled": True,
        #     "params": {
        #         "url": "https://api.fyndx1.de/masquerader/v1/aio-request-test/post",
        #         "data": {"key1": "val1"},
        #         "protocol": "HTTP",
        #         "protocol_info": {
        #             "request_type": "POST",
        #             "circuit_breaker_config": {
        #                 "retry_config": {
        #                     "name": "asdf",
        #                     "allowed_retries": 5
        #                 }
        #             },
        #         },
        #         "pre_processor_config": {
        #             "function": test,
        #             "async_enabled": True,
        #             "params": {
        #                 "url": "https://api.fyndx1.de/masquerader/v1/aio-request-test/post",
        #                 "data": {"key2": "val2"},
        #                 "protocol": "HTTP",
        #                 "protocol_info": {
        #                     "request_type": "POST",
        #                     "circuit_breaker_config": {
        #                         "retry_config": {
        #                             "name": "asdf",
        #                             "allowed_retries": 5
        #                         }
        #                     },
        #                 }
        #             }
        #         }
        #     }
        # },
        # post_processor_config={
        #     "function": request,
        #     "async_enabled": True,
        #     "params": {
        #         "url": "https://api.fyndx1.de/masquerader/v1/aio-request-test/post",
        #         "data": {"key1": "val1"},
        #         "protocol": "HTTP",
        #         "protocol_info": {
        #             "request_type": "POST",
        #             "circuit_breaker_config": {
        #                 "retry_config": {
        #                     "name": "asdf",
        #                     "allowed_retries": 5
        #                 }
        #             },
        #         },
        #         "post_processor_config": {
        #             "function": test,
        #             "async_enabled": True,
        #             "params": {
        #                 "url": "https://api.fyndx1.de/masquerader/v1/aio-request-test/post",
        #                 "data": {"key2": "val2"},
        #                 "protocol": "HTTP",
        #                 "protocol_info": {
        #                     "request_type": "POST",
        #                     "circuit_breaker_config": {
        #                         "retry_config": {
        #                             "name": "asdf",
        #                             "allowed_retries": 5
        #                         }
        #                     },
        #                 }
        #             }
        #         }
        #     }
        # }
    )
)
print(res)
