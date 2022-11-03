# Async HTTP / SOAP / FTP Request Library

This library provides the functionality to make async API calls via HTTP / SOAP / FTP protocols via a config.

### Installation
```pip install asyncio-requests ```

## HTTP

* Uses aiohttp internally
* Has an inbuilt circuit breaker
* Currently supports infinite nested depth of pre and post processors
* Retry Functionality
* Exceptions can be contributed in the utilities, and you can use your own exceptions in the circuit breaker config as well.
* Direct File Upload functionality.

Params -

<table>
  <tbody>
    <tr>
      <th class="Title" align="center">Param</th>
      <th class="Title" align="center">Data Type</th>
      <th class="Title" align="center">Optional/Required</th>
      <th class="Title" align="center">Help</th>
    </tr>
    <tr>
      <td align="center">url</td>
      <td align="center">Str</td>
      <td align="center">Required</td>
      <td align="center">URL to be hit</td>
    </tr>
    <tr>
      <td align="center">data</td>
      <td align="center">Dict</td>
      <td align="center">Optional</td>
      <td align="center">data to be sent. It can be dict or str. If dict, it will be dumped via ujson.dumps method</td>
    </tr>
    <tr>
      <td align="center">auth</td>
      <td align="center">auth object</td>
      <td align="center">Optional</td>
      <td align="center">Auth param is expected to be an auth object of your choice which is accepted by aiohttp. Eg - aiohttp.BasicAuth(username, password)</td>
    </tr>
    <tr>
      <td align="center">protocol</td>
      <td align="center">Str</td>
      <td align="center">Required</td>
      <td align="center">(HTTP/HTTPS/SOAP/FTP)</td>
    </tr>
    <tr>
      <td align="center">pre_processor_config</td>
      <td align="center">Dict</td>
      <td align="center">Optional</td>
      <td>
        <ul>
          <li>pre processor indicates an action (file download/api call or anything) to be done before making the actual API call.</li>
          <li>Takes async callable object which is executed before making the actual API call - Required</li>
          <li>Params dictionary where key is parameter to the callable object passed in pre processor and values is parameter value</li>
          <li>The callable object/function can be used from the utilities folder which is contributed by all or your own function address.</li>
          <li>You can nest the whole API. Eg - you can pass the address of asyncio_requests.request function too. The response will be a nested one. (Explained via example down)</li>
        </ul>
      </td>
    </tr>
    <tr>
      <td align="center">post_processor_config</td>
      <td align="center">Dict</td>
      <td align="center">Optional</td>
      <td>
        <ul>
          <li>post processor indicates an action (file download or delete file or api call or anything) to be done post making the actual API call.</li>
          <li>function: Takes async callable object/function address which is executed after making request - Required</li>
          <li>Params: Takes dictionary where key is parameter to the callable object/function passed in pre-processor and values is parameter value</li>
          <li>similar to pre-processor, difference being this is executed after making an API call.</li>
          <li>Eg - if you want to send the data of a file in the API call and the file needs to be downloaded. You can have a file download pre-processor function and have a file deletion post processor function.</li>
        </ul>
      </td>
    </tr>
    <tr aria-rowspan="12">
      <td align="center">protocol_info</td>
      <td align="center">Dict</td>
      <td align="center">Required</td>
      <td>
        <ul>
          <li>request_type - Str. Required. GET/PUT/POST/PATCH/DELETE/OPTIONS</li>
          <li>timeout -      Int. Optional. Default HTTP timeout is 15 seconds. Can be overridden if specified.</li>
          <li>certificate -  Tuple(str, str)  Optional. Used for SSL certificates and expected in the format Tuple('certificate path', 'certificate key path')</li>
          <li>verify_ssl -   Boolean. Optional. SSL is enabled by default</li>
          <li>cookies -      Str. Optional</li>
          <li>headers -      Dict. Required</li>
          <li>trace_config - List[tracer_callable_object] Optional. default tracer is aiohttp.TraceConfig() - Optional</li>
          <li>
            http_file_upload_config: Dict use this only if you want to send file in request. If you use this config then only file will be sent in request - Optional
            <ul>
              <li>local_filepath: machine file path for file to be sent in request</li>
              <li>file_key: The key in which the file data is to be sent</li>
            </ul>
          </li>serialization: serializer callable object. Optional. If you want to use any json serializer then you can pass here default is ujson.dumps.</li>
          <li>circuit_breaker_config - Dict - Optional
            <ul>
              <li>maximum_failures - Int. Optional. maximum failures you want to allow for request default is 5</li>
              <li>timeout - Int Optional. seconds timeout you want to keep for request default is 60 seconds</li>
              <li>retry_config - Dict - Optional
                <ul>
                  <li>name - Str required</li>
                  <li>allowed_retries - Int. Required this is for how many retries you want to perform</li>
                  <li>retriable_exceptions - List[<callable object of exception>]. Optional. list of exception types indicating which exceptions can cause a retry. If None every exception is considered retriable</li>
                  <li>abortable_exceptions - List[<callable object of exception>]. Optional. list of exception types indicating which exceptions should abort failsafe run immediately and be propagated out of failsafe. If None, no exception is considered abortable.</li>
                  <li>on_retries_exhausted - callable object. Optional. callable/function_address which will be invoked on retry exhausted event</li>
                  <li>on_failed_attempt - callable object. Optional. callable/function_address that will be invoked on a failed attempt event</li>
                  <li>on_abort - callable object. Optional. callable that will be invoked on an abort event</li>
                  <li>delay - Int Optional. seconds of delay between retries default is 0.</li> 
                  <li>max_delay - Int Optional. seconds of max delay between retries default 0</li>
                  <li>jitter: Boolean Optional. False when you want to keep the wait between calls constant else True</li>
                </ul>
              </li>
            </ul>
          </li>
        </ul>
      </td>
    </tr>
  </tbody>
</table>

Defaults - 
* By default, circuit breaker is not enabled and is activated only if provided with its config.
* By default, retry is not enabled and is activated only if provided with its config.
* Default Request tracer is enabled which provides the traces of the whole request wrt data chunks, dns cache hit etc.
* In case of user specific request tracer, a list of request tracer objects is expected which will override the default tracer.
* Default serialization is via ujson and can be overwritten by specifying one
* SSL is enabled by default

 

### How to Use
* Design the http request payload as per below format
* Mock url - https://api.fyndx1.de/masquerader/v1/aio-request-test/post is live and open for use.

```python
import aiohttp
from asyncio_requests.asyncio_request import request

await request(
    url="URL FOR REQUEST",  # str <Required>
    data={
        "key": "val"
    } or "",  # Data to be sent in body as dict or str,
    auth=aiohttp.BasicAuth('username', 'password'),  # This auth object is to be made by the user itself as there are n number of
    # auth mechanisms to add to. Eg - auth=aiohttp.BasicAuth(username, password). Its an Optional field.
    protocol="REQUEST PROTOCOL",  # str <Required> (HTTP/HTTPS)
    protocol_info={
        "request_type": "GET",  # str <Required>
        "timeout": 15,  # int <Optional> Default - 15
        "certificate": ('', ''),  # Tuple(str, str) <Optional>,
        "verify_ssl": True,  # Boolean <Optional>,
        "cookies": "",  # str <Optional>,
        "headers": {},  # dict <Optional>,
        "http_file_upload_config": {
            # optional Include only if you want call api with file. If this is included api body will have only file
            "local_filepath": "required",  # File path to be sent
            "file_key": "required",  # File to be sent on which key in request body
            "file_upload_chunk_size": "optional" # size of stream if streaming upload is required
            # After making API if you want to delete file then add value as True default is false.
        },
        "http_file_download_config": {
          "download_filepath": "required" # In case file downloads, location to which file is stored
          "file_download_chunk_size": "optional" # chunk size of a stream.
        }
        "circuit_breaker_config": {  # Optional
            "maximum_failures": int,  # Optional Failures allowed
            "timeout": int,  # Optional time in seconds
            "retry_config": {  # Optional Include this if you want retry API calls if failed on first time
                "name": str,  # Required Any name
                "allowed_retries": int,  # Required number of retries you want to make 
                "retriable_exceptions": [<callable object>] # Optional
                "abortable_exceptions": [<callable object>] # Optional
                "on_retries_exhausted": <callable object>, # Optional callable that will be invoked on a retries exhausted event,
                "on_failed_attempt": <callable object>, # Optional callable that will be invoked on a failed attempt event,
                "on_abort": <callable object>, # Optional callable that will be invoked on an abort event,
            "delay": int, # seconds of delay between retries Optional default 0,
            "max_delay": int, # seconds of max delay between retries Optional default 0,
        "jitter": bool # Boolean Optional,
            }
        }
    },
    pre_processor_config = {  # Optional
        "function": <callable object>,  # Required function that you want to call before http call
        "params": {  # Optional
            "param1": "value1" # Params you want to pass in function
        }
    },
    post_processor_config = {  # Optional
        "function": <callable object>,  # Required function that you want to call after http call 
        "params": {
            "param1": "value1" # Params you want to pass in function
        }
    }
)
```

* **Basic HTTP POST call**
```python
from asyncio_requests.asyncio_request import request


result = await request(
    url="https://api.fyndx1.de/masquerader/v1/aio-request-test/post",
    data={
        "first_name": "Joy",
        "last_name": "Pandey",
        "gender": "M"
    },
    protocol="HTTPS",
    protocol_info={
        "request_type": "POST"
    }
)

### Response
"""
{
  'url': 'https://api.fyndx1.de/masquerader/v1/aio-request-test/post',
  'payload': {
    'first_name': 'Joy',
    'last_name': 'Pandey',
    'gender': 'M'
  },
  'external_call_request_time': '2022-02-17 17:25:03.930531+05:30',
  'text': '',
  'error_message': '',
  'api_response': {
    'status_code': 200,
    'headers': {
      'Date': 'Thu, 17 Feb 2022 11:55:04 GMT',
      'Content-Type': 'application/json',
      'Content-Length': '57',
      'Connection': 'keep-alive',
      'X-Fynd-Trace-Id': '78ca02ff444ae5855e856c5f3d769364'
    },
    'cookies': {
      
    },
    'content': b'{"method": "POST", "status": true, "error_message": null}',
    'text': '{"method": "POST", "status": true, "error_message": null}',
    'json': {
      'method': 'POST',
      'status': True,
      'error_message': None
    },
    'request_tracer': [
      {
        'on_request_start': 287753.868594354,
        'is_redirect': False,
        'on_connection_create_start': 0.0002811980084516108,
        'on_dns_cache_miss': 0.002910615992732346,
        'on_dns_resolvehost_start': 0.0029266909696161747,
        'on_dns_resolvehost_end': 0.04894679499557242,
        'on_connection_create_end': 0.15098483895417303,
        'on_request_chunk_sent': 0.15202936198329553,
        'on_request_end': 0.2799108889885247
      }
    ]
  }
}
"""
```

* **API call with circuit breaker and custom exceptions**
```python
from asyncio_requests.asyncio_request import request


class HTTPRequestFailedException(Exception):
    pass


class CustomException(Exception):
    pass


def retry_exhausted_actions():
    print("All retries exhausted. API call failed.")
    
    
def request_attempt_failed_actions():
    print("API call failed.")
    
    
def request_abort_actions():
    print("API call aborted")


result = await request(
    url="https://api.fyndx1.de/masquerader/v1/aio-request-test/post",
    data={
        "first_name": "Joy",
        "last_name": "Pandey",
        "gender": "M"
    },
    protocol="HTTPS",
    protocol_info={
        "request_type": "POST",
        "circuit_breaker_config": {
            "maximum_failures": 5,
            "timeout": 15,
            "retry_config": {
                "name": "retry_masquerader",
                "allowed_retries": 5,
                "retriable_exceptions": [HTTPRequestFailedException],
                "abortable_exceptions": [CustomException],
                "on_retries_exhausted": retry_exhausted_actions,
                "on_failed_attempt": request_attempt_failed_actions,
                "on_abort": request_abort_actions,
                "delay": 5,
                "max_delay": 300,
                "jitter": True
            }
        }
    }
)

### Value of result
"""
{
  'url': 'https://api.fyndx1.de/masquerader/v1/aio-request-test/post',
  'payload': {
    'first_name': 'Joy',
    'last_name': 'Pandey',
    'gender': 'M'
  },
  'external_call_request_time': '2022-02-18 12:57:20.762713+05:30',
  'text': '',
  'error_message': '',
  'api_response': {
    'status_code': 200,
    'headers': {
      'Date': 'Fri, 18 Feb 2022 07:27:21 GMT',
      'Content-Type': 'application/json',
      'Content-Length': '57',
      'Connection': 'keep-alive',
      'X-Fynd-Trace-Id': '390cd5e9f4b1f179d5d711ca7bc83ec3'
    },
    'cookies': {
      
    },
    'content': b'{"method": "POST", "status": true, "error_message": null}',
    'text': '{"method": "POST", "status": true, "error_message": null}',
    'json': {
      'method': 'POST',
      'status': True,
      'error_message': None
    },
    'request_tracer': [
      {
        'on_request_start': 352622.180567606,
        'is_redirect': False,
        'on_connection_create_start': 0.0009668020065873861,
        'on_dns_cache_miss': 0.07304156001191586,
        'on_dns_resolvehost_start': 0.07307461701566353,
        'on_dns_resolvehost_end': 0.31564718199661,
        'on_connection_create_end': 0.5526716759777628,
        'on_request_chunk_sent': 0.5531467269756831,
        'on_request_end': 0.6851100819767453
      }
    ]
  }
}
"""
```

* **API with pre and post processor enabled with circuit breaker and retries.**
```python
from asyncio_requests.asyncio_request import request
from typing import Dict, Text


async def make_request_payload(response: Dict, first_name: Text, last_name: Text, gender: Text):
    response["payload"] = {
        "first_name": first_name,
        "last_name": last_name,
        "gender": gender
    }


async def print_response_recieved_from_api(response: Dict, text: Text):
    print(f"{text}{response['api_response']}")


result = await request(
    url="https://api.fyndx1.de/masquerader/v1/aio-request-test/post",
    protocol="HTTPS",
    protocol_info={
        "request_type": "POST",
        "circuit_breaker_config": {
            "timeout": 150,
            "retry_config": {
                "name": "api_retry",
                "allowed_retries": 4
            }
        }
    },
    pre_processor_config={
        "function": make_request_payload,
        "params": {
            "first_name": "Joy",
            "last_name": "Pandey",
            "gender": "M"
        }
    },
    post_processor_config={
        "function": print_response_recieved_from_api,
        "params": {
            "text": "Response received from API: "
        }
    }
)

### Response
### The pre and post processor keys have no values in response since they were just print statements. Had they been API calls, the value would have been different.
### The print statements will be printed in the shell if run but won't have its resemblence in the response.
"""
{
  'url': 'https://api.fyndx1.de/masquerader/v1/aio-request-test/post',
  'payload': {
    'first_name': 'Joy',
    'last_name': 'Pandey',
    'gender': 'M'
  },
  'external_call_request_time': '2022-02-17 17:33:35.508376+05:30',
  'text': '',
  'error_message': '',
  'pre_processor_response': None,
  'api_response': {
    'status_code': 200,
    'headers': {
      'Date': 'Thu, 17 Feb 2022 12:03:35 GMT',
      'Content-Type': 'application/json',
      'Content-Length': '57',
      'Connection': 'keep-alive',
      'X-Fynd-Trace-Id': '8903eeb30ed218385631d3b52d04b38e'
    },
    'cookies': {
      
    },
    'content': b'{"method": "POST", "status": true, "error_message": null}',
    'text': '{"method": "POST", "status": true, "error_message": null}',
    'json': {
      'method': 'POST',
      'status': True,
      'error_message': None
    },
    'request_tracer': [
      {
        'on_request_start': 288265.446420053,
        'is_redirect': False,
        'on_connection_create_start': 0.00028238497907295823,
        'on_dns_cache_miss': 0.0028724189614877105,
        'on_dns_resolvehost_start': 0.002888173970859498,
        'on_dns_resolvehost_end': 0.09302646096330136,
        'on_connection_create_end': 0.2075990799930878,
        'on_request_chunk_sent': 0.20890663599129766,
        'on_request_end': 0.319920428970363
      }
    ]
  },
  'post_processor_response': None
}
"""
```

* **Having separate API call in pre-processor.**
* This is usually the case wherein we want to report some data before making the actual API call
```python
from asyncio_requests.asyncio_request import request

result = await request(
    url="https://api.fyndx1.de/masquerader/v1/aio-request-test/post",
    data={
        "first_name": "Joy",
        "last_name": "Pandey",
        "gender": "M"
    },
    protocol="HTTPS",
    protocol_info={
        "request_type": "POST"
    },
    pre_processor_config={
        "function": request,
        "async_enabled": True,
        "params": {
            "url": "https://api.fyndx1.de/masquerader/v1/aio-request-test/post",
            "data": {
                "first_name": "Joy",
                "last_name": "Pandey",
                "Gender": "M"
            },
            "protocol": "HTTP",
            "protocol_info": {
                "request_type": "POST"
            }
        }
    }
)

### Value of result
"""
{
  'url': 'https://api.fyndx1.de/masquerader/v1/aio-request-test/post',
  'payload': {
    'first_name': 'Joy',
    'last_name': 'Pandey',
    'gender': 'M'
  },
  'external_call_request_time': '2022-02-18 13:26:35.575362+05:30',
  'text': '',
  'error_message': '',
  'pre_processor_response': {
    'url': 'https://api.fyndx1.de/masquerader/v1/aio-request-test/post',
    'payload': {
      'first_name': 'Joy',
      'last_name': 'Pandey',
      'Gender': 'M'
    },
    'external_call_request_time': '2022-02-18 13:26:35.575469+05:30',
    'text': '',
    'error_message': '',
    'api_response': {
      'status_code': 200,
      'headers': {
        'Date': 'Fri, 18 Feb 2022 07:56:36 GMT',
        'Content-Type': 'application/json',
        'Content-Length': '57',
        'Connection': 'keep-alive',
        'X-Fynd-Trace-Id': 'ae2703a4c82e8f917c53faded0688717'
      },
      'cookies': {},
      'content': b'{"method": "POST", "status": true, "error_message": null}',
      'text': '{"method": "POST", "status": true, "error_message": null}',
      'json': {
        'method': 'POST',
        'status': True,
        'error_message': None
      },
      'request_tracer': [
        {
          'on_request_start': 354376.993160197,
          'is_redirect': False,
          'on_connection_create_start': 0.00041024398524314165,
          'on_dns_cache_miss': 0.004407248983625323,
          'on_dns_resolvehost_start': 0.0044287089840509,
          'on_dns_resolvehost_end': 0.32443026901455596,
          'on_connection_create_end': 0.44923901598667726,
          'on_request_chunk_sent': 0.449799319030717,
          'on_request_end': 0.5300842020078562
        }
      ]
    }
  },
  'api_response': {
    'status_code': 200,
    'headers': {
      'Date': 'Fri, 18 Feb 2022 07:56:36 GMT',
      'Content-Type': 'application/json',
      'Content-Length': '57',
      'Connection': 'keep-alive',
      'X-Fynd-Trace-Id': 'ddb370fbf58999c359fe384b547446c9'
    },
    'cookies': {},
    'content': b'{"method": "POST", "status": true, "error_message": null}',
    'text': '{"method": "POST", "status": true, "error_message": null}',
    'json': {
      'method': 'POST',
      'status': True,
      'error_message': None
    },
    'request_tracer': [
      {
        'on_request_start': 354377.524928869,
        'is_redirect': False,
        'on_connection_create_start': 0.000421632023062557,
        'on_dns_cache_miss': 0.00067474803654477,
        'on_dns_resolvehost_start': 0.0006999420002102852,
        'on_dns_resolvehost_end': 0.002583371999207884,
        'on_connection_create_end': 0.09995210904162377,
        'on_request_chunk_sent': 0.10060718702152371,
        'on_request_end': 0.2261603070073761
      }
    ]
  }
}
"""
```

* **API call with nested pre and post processors**
* Here the pre processor(parent) has another pre-processor(child) within it.
* The response will include all the nested responses in the same fashion as that of the config set
* The actual flow would be (child pre-processor -> parent pre-processor -> main API call -> parent post-processor -> child post processor)
* response format will be this way -
```
    parent pre-processor response
        child pre processor response
            child's child pre preprocesor response
                infinite nesting...
    
    main api call response
    
    parent post-processor response
        child post processor response
            child's child post preprocesor response
                infinite nesting...
```

```python
from asyncio_requests.asyncio_request import request


async def test_fun(*args, **kwargs):
    return {"text": "final res"}


result = await request(
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
    },
    pre_processor_config={
        "function": request,
        "async_enabled": True,
        "params": {
            "url": "https://api.fyndx1.de/masquerader/v1/aio-request-test/post",
            "data": {
                "first_name": "Joy",
                "last_name": "Pandey",
                "Gender": "M"
            },
            "protocol": "HTTP",
            "protocol_info": {
                "request_type": "POST",
                "circuit_breaker_config": {
                    "retry_config": {
                        "name": "asdf",
                        "allowed_retries": 5
                    }
                },
            },
            "pre_processor_config": {
                "function": test_fun,
                "async_enabled": True,
                "params": {
                    "url": "https://api.fyndx1.de/masquerader/v1/aio-request-test/post",
                    "data": {
                        "first_name": "Joy",
                        "last_name": "Pandey",
                        "Gender": "M"
                    },
                    "protocol": "HTTP",
                    "protocol_info": {
                        "request_type": "POST",
                        "circuit_breaker_config": {
                            "retry_config": {
                                "name": "asdf",
                                "allowed_retries": 5
                            }
                        },
                    }
                }
            }
        }
    },
    post_processor_config={
        "function": request,
        "async_enabled": True,
        "params": {
            "url": "https://api.fyndx1.de/masquerader/v1/aio-request-test/post",
            "data": {
                "first_name": "Joy",
                "last_name": "Pandey",
                "Gender": "M"
            },
            "protocol": "HTTP",
            "protocol_info": {
                "request_type": "POST",
                "circuit_breaker_config": {
                    "retry_config": {
                        "name": "asdf",
                        "allowed_retries": 5
                    }
                },
            },
            "post_processor_config": {
                "function": test_fun,
                "async_enabled": True,
                "params": {
                    "url": "https://api.fyndx1.de/masquerader/v1/aio-request-test/post",
                    "data": {
                        "first_name": "Joy",
                        "last_name": "Pandey",
                        "Gender": "M"
                    },
                    "protocol": "HTTP",
                    "protocol_info": {
                        "request_type": "POST",
                        "circuit_breaker_config": {
                            "retry_config": {
                                "name": "asdf",
                                "allowed_retries": 5
                            }
                        },
                    }
                }
            }
        }
    }
)

### Response
"""
{
  'url': 'https://api.fyndx1.de/masquerader/v1/aio-request-test/post',
  'payload': {
    'first_name': 'Joy',
    'last_name': 'Pandey',
    'Gender': 'M'
  },
  'external_call_request_time': '2022-02-17 17:22:01.383304+05:30',
  'text': '',
  'error_message': '',
  'pre_processor_response': {
    'url': 'https://api.fyndx1.de/masquerader/v1/aio-request-test/post',
    'payload': {
      'first_name': 'Joy',
      'last_name': 'Pandey',
      'Gender': 'M'
    },
    'external_call_request_time': '2022-02-17 17:22:01.383358+05:30',
    'text': '',
    'error_message': '',
    'pre_processor_response': {
      'text': 'final res'
    },
    'api_response': {
      'status_code': 200,
      'headers': {
        'Date': 'Thu, 17 Feb 2022 11:52:01 GMT',
        'Content-Type': 'application/json',
        'Content-Length': '57',
        'Connection': 'keep-alive',
        'X-Fynd-Trace-Id': 'b1a3111270067ae160eeaf9971b04cc5'
      },
      'cookies': {
        
      },
      'content': b'{"method": "POST", "status": true, "error_message": null}',
      'text': '{"method": "POST", "status": true, "error_message": null}',
      'json': {
        'method': 'POST',
        'status': True,
        'error_message': None
      },
      'request_tracer': [
        {
          'on_request_start': 287571.321608293,
          'is_redirect': False,
          'on_connection_create_start': 0.00031328899785876274,
          'on_dns_cache_miss': 0.0029667950002476573,
          'on_dns_resolvehost_start': 0.0029829980339854956,
          'on_dns_resolvehost_end': 0.0064852479845285416,
          'on_connection_create_end': 0.08529951400123537,
          'on_request_chunk_sent': 0.0858444279874675,
          'on_request_end': 0.1671372150303796
        }
      ]
    }
  },
  'api_response': {
    'status_code': 200,
    'headers': {
      'Date': 'Thu, 17 Feb 2022 11:52:01 GMT',
      'Content-Type': 'application/json',
      'Content-Length': '57',
      'Connection': 'keep-alive',
      'X-Fynd-Trace-Id': '3340481533a6511b15952cabb4c144bb'
    },
    'cookies': {
      
    },
    'content': b'{"method": "POST", "status": true, "error_message": null}',
    'text': '{"method": "POST", "status": true, "error_message": null}',
    'json': {
      'method': 'POST',
      'status': True,
      'error_message': None
    },
    'request_tracer': [
      {
        'on_request_start': 287571.490459029,
        'is_redirect': False,
        'on_connection_create_start': 0.0006432340014725924,
        'on_dns_cache_miss': 0.00104641099460423,
        'on_dns_resolvehost_start': 0.001091104990337044,
        'on_dns_resolvehost_end': 0.0037200640072114766,
        'on_connection_create_end': 0.10335264401510358,
        'on_request_chunk_sent': 0.10410607699304819,
        'on_request_end': 0.18950222100829706
      }
    ]
  },
  'post_processor_response': {
    'url': 'https://api.fyndx1.de/masquerader/v1/aio-request-test/post',
    'payload': {
      'first_name': 'Joy',
      'last_name': 'Pandey',
      'Gender': 'M'
    },
    'external_call_request_time': '2022-02-17 17:22:01.743288+05:30',
    'text': '',
    'error_message': '',
    'api_response': {
      'status_code': 200,
      'headers': {
        'Date': 'Thu, 17 Feb 2022 11:52:02 GMT',
        'Content-Type': 'application/json',
        'Content-Length': '57',
        'Connection': 'keep-alive',
        'X-Fynd-Trace-Id': 'a0304896aabbc394894d442fa27a5c3e'
      },
      'cookies': {
        
      },
      'content': b'{"method": "POST", "status": true, "error_message": null}',
      'text': '{"method": "POST", "status": true, "error_message": null}',
      'json': {
        'method': 'POST',
        'status': True,
        'error_message': None
      },
      'request_tracer': [
        {
          'on_request_start': 287571.681455504,
          'is_redirect': False,
          'on_connection_create_start': 0.00041248503839597106,
          'on_dns_cache_miss': 0.0006613450241275132,
          'on_dns_resolvehost_start': 0.0006853759987279773,
          'on_dns_resolvehost_end': 0.0024919320130720735,
          'on_connection_create_end': 0.08381915499921888,
          'on_request_chunk_sent': 0.08448734600096941,
          'on_request_end': 0.5899507160065696
        }
      ]
    },
    'post_processor_response': {
      'text': 'final res'
    }
  }
}
"""
```

* **API call to send a file**
* Here we are downloading a file in the pre-processor. If the file is already present in the system then you can avoid that pre-processor and directly mention the file address in the local_file_path variable.
* The file can be downloaded by using the existing pre processor function in the utilities.
* The Utilities dir has a function that supports file download via url/aws s3.
* The Utilities dir also has a function to delete a file. If you want to delete teh file post making the API call, use this in the post processor.
* If you have some other way around to download the file, just pass that function address in the pre processor and include the file address in the local_file_path variable.

```python
from asyncio_requests.asyncio_request import request
from asyncio_requests.utils.http_file_upload_config import download_file_from_url, delete_local_file_path


local_file_path = "/tmp/test.pdf"
result = await request(
    url="http://localhost:5000/api/v1/test/aio-request-files",
    protocol="HTTPS",
    protocol_info={
        "request_type": "POST",
        "http_file_upload_config": {
            "local_filepath": local_file_path,
            "file_key": "file"
        }
    },
    pre_processor_config={
        "function": download_file_from_url,
        "params": {
            "file_download_path": "https://didukhn.github.io/homepage/assets/img/photo.jpg",
            "local_filepath": local_file_path
        }
    },
    post_processor_config={
        "function": delete_local_file_path,
        "params": {
            "local_filepath": local_file_path
        }
    }
)

### Response
"""
{
  'url': 'http://localhost:5000/api/v1/test/aio-request-files',
  'payload': {
    
  },
  'external_call_request_time': '2022-02-17 17:13:03.231826+05:30',
  'text': '',
  'error_message': '',
  'pre_processor_response': None,
  'api_response': {
    'status_code': 200,
    'headers': {
      'Connection': 'close',
      'Content-Length': '29',
      'Content-Type': 'application/json'
    },
    'cookies': {
      
    },
    'content': b'{"success":true,"message":""}',
    'text': '{"success":true,"message":""}',
    'json': {
      'success': True,
      'message': ''
    },
    'request_tracer': [
      {
        'on_request_start': 287033.4935145,
        'is_redirect': False,
        'on_connection_create_start': 0.0021707930136471987,
        'on_dns_cache_miss': 0.002449413004796952,
        'on_dns_resolvehost_start': 0.002480961033143103,
        'on_dns_resolvehost_end': 0.003233974042814225,
        'on_connection_create_end': 0.0042467640014365315,
        'on_request_chunk_sent': 0.0064254660392180085,
        'on_request_end': 0.1773580180015415
      }
    ]
  },
  'post_processor_response': None
}
"""
```

**Utilities Included**
* Download a file from AWS S3
* Download a file from public url
* Delete a local file on system


## FTP

* Uses aioftp internally to implement FTP/FTPS.
* Added functionality of circuit breaker, pre and post processor configs same as http.
* Can Leverage all the ftp commands provided by aioftp library.
* By Default used FTP protocol can use FTPS if ssl config is enabled.


# How to use.

```python
import aiohttp
from asyncio_requests.asyncio_request import request

await request(
    url="Server Ip",  # Ip/url or ftp server <Required>
    auth=aiohttp.BasicAuth('username', 'password'),  # The username and ip of the ftp server, to be sent as aiohttp.BasicAuth object <Required>
    protocol="FTP",  # str <Required> (FTP)
    protocol_info={
        "port": 21, # default is 21 <Optional>
        "command": "download", # generic ftp commands like download, upload, remove <Required>
        "server_path": "/tmp/temp.pdf", # path from where to get/remove or upload file on server.
        "client_path": "", # path where file is downloaded/uploaded to. <optional>
        "timeout": 30 # <Optional>
        "verify_ssl": False # default is False <Optional>
        "certificate" "" # required if verify_ssl is True
        "circuit_breaker_config": {  # Optional
            "maximum_failures": int,  # Optional Failures allowed
            "timeout": int,  # Optional time in seconds
            "retry_config": {  # Optional Include this if you want retry calls if failed on first time
                "name": str,  # Required Any name
                "allowed_retries": int,  # Required number of retries you want to make
                "retriable_exceptions": [<callable object>] # Optional
                "abortable_exceptions": [<callable object>] # Optional
                "on_retries_exhausted": <callable object>, # Optional callable that will be invoked on a retries exhausted event,
                "on_failed_attempt": <callable object>, # Optional callable that will be invoked on a failed attempt event,
                "on_abort": <callable object>, # Optional callable that will be invoked on an abort event,
            "delay": int, # seconds of delay between retries Optional default 0,
            "max_delay": int, # seconds of max delay between retries Optional default 0,
            "jitter": bool # Boolean Optional,
          }
      }
    },
    pre_processor_config = {  # Optional
        "function": <callable object>,  # Required function that you want to call before ftp call
        "params": {  # Optional
            "param1": "value1" # Params you want to pass in function
        }
    },
    post_processor_config = {  # Optional
        "function": <callable object>,  # Required function that you want to call after ftp call
        "params": {
            "param1": "value1" # Params you want to pass in function
        }
    }
)
```

# Sample FTP Call.

```python
import aiohttp
from asyncio_requests.asyncio_request import request
from asyncio_requests.utils.http_file_upload_config import download_file_from_url

local_path = "/tmp/temp.png"
await request(
    url = "localhost",
    auth = aiohttp.BasicAuth("use","pswd"),
    protocol = "FTP",
    protocol_info = {
        "port": 21,
        "command": "upload",
        "server_path": "/home/resources/logo.png",
        "client_path": local_path,
        "circuit_breaker_config": {
            "timeout": 150,
            "retry_config": {
                "name": "api_retry",
                "allowed_retries": 4
            }
        }
    },
    pre_processor_config = {
        "function": download_file_from_s3,
          "params": {
            "file_download_path": "https://[bucket_name].s3.amazonaws.com/logo.png",
            "local_filepath": local_path
          }
    }
)

## Resonse
"""
{'api_response': True,
 'error_message': '',
 'external_call_request_time': '2022-05-13 19:07:35.775706+05:30',
 'file': '/home/resources/logo.png',
 'file_stats': {'modify': '20220513190700',
                'size': '29304',
                'type': 'file',
                'unix.group': '1000',
                'unix.links': '1',
                'unix.mode': 436,
                'unix.owner': '1000'},
 'mode': 'upload',
 'payload': {'success': True},
 'pre_processor_response': None,
 'text': '',
 'url': 'localhost'}

"""

```


## SOAP
(upcoming)


### Generating Distribution Archives

```bash
python3 -m pip install --upgrade setuptools wheel
python3 setup.py sdist bdist_wheel
```
This command should output a lot of text and once completed should generate two files in the `dist` directory.

## Open Source contribution 

You can add utilities that can be used by others. 

Eg - Contributing a function that accepts certain params and downloads a file via AWS S3.
This function can be used by other developers in the pre/post processor to download the file before or after making the API call.

**Make sure to add the utility in the utilities section in the readme wrt protocol.**

### Generating New Tags/Release

 - Check the code with flake8, mypy, bandit, pytest before submitting a PR
 - Update version in [setup.py](setup.py)
 - Update version in [docs/source/conf.py](docs/source/conf.py)
 - Update version in README.md section
 - Send a PR, and after it gets merged to master create a tag from master in the format `vX.Y`
   - `X` - Major Release (Breaking Changes)
   - `Y` - Minor Release
 

**To know more about the developer, here's a quote to find him out -** 
```Anton died so we could live```