from logic_test import logic_test
from aio_requests.aio_request import request
import asyncio


async def test(**kwargs):
    return kwargs


res = asyncio.run(
    request(
        url="https://api.fyndx1.de/masquerader/v3/shipments/flipkart1250",
        data={
            "key0": "val0"
        },
        protocol="HTTP",
        protocol_info={
            "request_type": "GET",
            "verify_ssl": True,
            "circuit_breaker_config": {
                "retry_config": {
                    "name": "asdf",
                    "allowed_retries": 5
                }
            }
        },
        # pre_processor_config={
        #     "func_addr": logic_test,
        #     "async_enabled": True,
        #     "params": {
        #         "url": "https://api.fyndx1.de/masquerader/v3/shipments/flipkart1259",
        #         "data": {"key1": "val1"},
        #         "protocol": "HTTP",
        #         "protocol_info": {"request_type": "GET"},
        #         "pre_processor_config": {
        #             "func_addr": test,
        #             "async_enabled": True,
        #             "params": {
        #                 "url": "https://api.fyndx1.de/masquerader/v3/shipments/flipkart1258",
        #                 "data": {"key2": "val2"},
        #                 "protocol": "HTTP",
        #                 "protocol_info": {"request_type": "GET"}
        #             }
        #         }
        #     }
        # },
        # post_processor_config={
        #     "func_addr": logic_test,
        #     "async_enabled": True,
        #     "params": {
        #         "url": "https://api.fyndx1.de/masquerader/v3/shipments/flipkart1259",
        #         "data": {"key1": "val1"},
        #         "protocol": "HTTP",
        #         "protocol_info": {"request_type": "GET"},
        #         "post_processor_config": {
        #             "func_addr": test,
        #             "async_enabled": True,
        #             "params": {
        #                 "url": "https://api.fyndx1.de/masquerader/v3/shipments/flipkart1258",
        #                 "data": {"key2": "val2"},
        #                 "protocol": "HTTP",
        #                 "protocol_info": {"request_type": "GET"}
        #             }
        #         }
        #     }
        # }
    )
)
print(res)
