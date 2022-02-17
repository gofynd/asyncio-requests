from aio_requests.aio_request import request
import asyncio
from aio_requests.utils.http_file_config import download_file_from_url, delete_local_file_path


async def test(*args, **kwargs):
    return {"text": "final res"}


# https://api.fyndx1.de/masquerader/v1/aio-request-test/get
# https://api.fyndx1.de/masquerader/v1/aio-request-test/post
# https://api.fyndx1.de/masquerader/v1/aio-request-test/put
# https://api.fyndx1.de/masquerader/v1/aio-request-test/delete
# http://localhost:5000/api/v1/test/aio-request-files
local_file_path = "/tmp/test.pdf"


res = asyncio.run(
    request(
        url="https://api.fyndx1.de/masquerader/v1/aio-request-test/post",
        data={
            "first_name": "Joy",
            "last_name": "Pandey",
            "Gender": "M"
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
            # "http_file_config": {
            #     "local_filepath": local_file_path,
            #     "file_key": "file"
            # }
        },
        # pre_processor_config={
        #     "function": download_file_from_url,
        #     "params": {
        #         "file_download_path": "https://s3.ap-south-1.amazonaws.com/fynd-platform-test-mumbai/trell-3000008556-label-1643895203.pdf",
        #         "local_filepath": local_file_path
        #     }
        # },
        # post_processor_config={
        #     "function": delete_local_file_path,
        #     "params": {
        #         "local_filepath": local_file_path
        #     }
        # }
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
print()
print()
print()
print(res)


res = asyncio.run(
    request(
        url="https://api.fyndx1.de/masquerader/v1/aio-request-test/post",
        data={
            "first_name": "Joy",
            "last_name": "Pandey",
            "Gender": "M"
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
            }
        }
    )
)
print()
print()
print()
print(res)
