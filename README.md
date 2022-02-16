# Fynd Async HTTP Request Library

This library provides the functionality to make async API calls via HTTP / SOAP / FTP protocols via a config.

**Open Source contribution -** 

You can add utilities that can be used by others. 

Eg - Contributing a function that accepts certain params and downloads a file via AWS S3.
This function can be used by other developers in the pre/post processor to download the file before or after making the API call.

**Make sure to add the utility in the utilities section in the readme wrt protocol.**

### HTTP

* Uses aiohttp internally
* Has an inbuilt circuit breaker
* Currently supports infinite nested depth of pre and post processors
* Retry Functionality
* Exceptions can be contributed in the utilities and you can use your own exceptions in the circuit breaker config as well.

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
          <li>Takes async function address which is executed before making the actual API call - Required</li>
          <li>Params dictionary where key is parameter to the function passed in pre processor and values is parameter value</li>
          <li>The function address can be used from the utilities folder which is contributed by all or your own function address.</li>
          <li>You can nest the whole API. Eg - you can pass the address of aio_requests.request function too. The response will be a nested one. (Explained via example down)</li>
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
          <li>function: Takes async function address which is executed after making request - Required</li>
          <li>Params: Takes dictionary where key is parameter to the function passed in pre processor and values is parameter value</li>
          <li>similar to pre processor, difference being this is executed after making an API call.</li>
          <li>Eg - if you want to send the data of a file in the API call and the file needs to be downloaded. You can have a file download pre processor functionand have a file deletion post processor function.</li>
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
          <li>timeout -      Int. Optional. Default HTTP timeout is 15 seconds. Can be overriden if specified.</li>
          <li>certificate -  Tuple(str, str)  Optional. Used for SSL certificates and expected in the format Tuple('certificate path', 'certificate key path')</li>
          <li>verify_ssl -   Boolean. Optional. SSL is enabled by default</li>
          <li>cookies -      Str. Optional</li>
          <li>headers -      Dict. Required</li>
          <li>trace_config - List[tracer_function] Optional. request tracer object if want use request tracer default tracer is aiohttp.TraceConfig() - Optional</li>
          <li>
            http_file_config: Dict use this only if you want to send file in request. If you use this config then only file will be sent in request - Optional
            <ul>
              <li>local_filepath: machine file path for file to be sent in request</li>
              <li>file_key: The key in which the file data is to be sent</li>
            </ul>
          </li>serialization: serializer function address. Optional. If you want to use any json serializer then you can pass here default is ujson.dumps.</li>
          <li>circuit_breaker_config - Dict - Optional
            <ul>
              <li>maximum_failures - Int. Optional. maximum failures you want to allow for request default is 5</li>
              <li>timeout - Int Optional. seconds timeout you want to keep for request default is 60 seconds</li>
              <li>retry_config - Dict - Optional
                <ul>
                  <li>name - Str required</li>
                  <li>allowed_retries - Int. Required this is for how many retries you want to perform</li>
                  <li>retriable_exceptions - List[function address of exception]. Optional. list of Exceptions on which you want to retry.
                  <li>abortable_exceptions - List[function address of exception]. list of Exceptions on which exception the request to be aborted</li>
                  <li>on_retries_exhausted - function address. Optional. callable/function_address which will be invoked on retry exhausted event</li>
                  <li>on_failed_attempt - function address. Optional. callable/function_address that will be invoked on a failed attempt event</li>
                  <li>on_abort - function address. Optional. callable that will be invoked on an abort event</li>
                  <li>delay - Int Optional. seconds of delay between retries default is 0.</li> 
                  <li>max_delay - Int Optional. seconds of max delay between retries default 0</li>
                  <li>jitter: Boolean Optional</li>
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
```python
from aio_request import request


await request(
    url="URL FOR REQUEST",  # str <Required>
    data={
        "key": "val"
    } or "" # Data to be sent in body as dict or str,
    auth=auth_object,  # This auth object is to be made by the user itself as there are n number of
         # auth mechanisms to add to. Eg - auth=aiohttp.BasicAuth(username, password)
    protocol="REQUEST PROTOCOL", # str <Required> (HTTP/HTTPS)
    protocol_info={
        "request_type": "GET", #str <Required>
        "timeout": 15,  # int <Optional> Default - 15
        "certificate: ('', ''),  #Tuple(str, str) <Optional>,
        "verify_ssl": True, # Boolean <Optional>,
        "cookies": "", # str <Optional>,
        "headers": {},  # dict <Optional>,
        "http_file_config": {  #optional Include only if you want call api with file. If this is included api body will have only file
            "local_filepath": "required",  # File path to be sent
            "file_key": "required",  # File to be sent on which key in request body
            "delete_local_file": "boolean Optional"  # After making API if you want to delete file then add value as True default is false.
        },
        "circuit_breaker_config": {  # Optional
            "maximum_failures": int,  # Optional Failures allowed
            "timeout": int,  # Optional time in seconds
            "retry_config": {  # Optional Include this if you want retry API calls if failed on first time
                "name": str,  # Required Any name
                "allowed_retries": int,  # Required number of retries you want to make 
                "retriable_exceptions": [Optional list of Exceptions],
                "abortable_exceptions": [Optional list of Exceptions],
                "on_retries_exhausted": Optional callable that will be invoked on a retries exhausted event,
                "on_failed_attempt": Optional callable that will be invoked on a failed attempt event,
                "on_abort": Optional callable that will be invoked on an abort event,
                "delay": int seconds of delay between retries Optional default 0,
                "max_delay": int seconds of max delay between retries Optional default 0,
                "jitter": Boolean Optional,
            } 
        }
    },
    pre_processor_config={  # Optional
        "function": function_address, # Required function that you want to call before http call
        "params": {  # Optional
            "param1": "value1"
            # Params you want to pass in function
        } 
    },
    post_processor_config={  # Optional
       "function": function_address,  # Required function that you want to call after http call 
       "params": {
          "param1": "value1"
          # Params you want to pass in function
       }
    }
)
```


**Utilities Included**
* Download a file from AWS S3



### How To Use
```python
from aio_request import request

await request(
    url="URL FOR REQUEST",
    data={
        "key": "val"
        # Data to be sent in body
    },
    auth=("Username", "password").  # Tuple (username, password) for basic auth - Optional field
    protocol="REQUEST PROTOCOL", # HTTP/HTTPS
    protocol_info={
        "request_type": "GET", #required
        "timeout": int,  #Optional
        "certificate: "",  #Optional,
        "verify_ssl": Boolean,  #Optional,
        "cookies": "",  #Optional,
        "headers": {},  #Optional,
        "http_file_config": {  #optional Include only if you want call api with file. If this is included api body will have only file
            "local_filepath": "required",  # File path to be sent
            "file_key": "required",  # File to be sent on which key in request body
            "delete_local_file": "boolean Optional"  # After making API if you want to delete file then add value as True default is false.
        },
        "circuit_breaker_config": {  # Optional
            "maximum_failures": int,  # Optional Failures allowed
            "timeout": int,  # Optional time in seconds
            "retry_config": {  # Optional Include this if you want retry API calls if failed on first time
                "name": str,  # Required Any name
                "allowed_retries": int,  # Required number of retries you want to make 
                "retriable_exceptions": [Optional list of Exceptions],
                "abortable_exceptions": [Optional list of Exceptions],
                "on_retries_exhausted": Optional callable that will be invoked on a retries exhausted event,
                "on_failed_attempt": Optional callable that will be invoked on a failed attempt event,
                "on_abort": Optional callable that will be invoked on an abort event,
                "delay": int seconds of delay between retries Optional default 0,
                "max_delay": int seconds of max delay between retries Optional default 0,
                "jitter": Boolean Optional,
            } 
        }
    },
    pre_processor_config={  # Optional
        "function": function_address, # Required function that you want to call before http call
        "params": {  # Optional
            "param1": "value1"
            # Params you want to pass in function
        } 
    },
    post_processor_config={  # Optional
       "function": function_address,  # Required function that you want to call after http call 
       "params": {
          "param1": "value1"
          # Params you want to pass in function
       }
    }
)
```


### Log Request Metric
If `log_request_metric` key is set and send along with request gives trace as below for the request     

```
  2019-08-05 22:12:07,975-fynd_logger.py-INFO-{
 "app_ist_log_datetime": "2019-08-05 22:12:07.974752",           
 "app_ist_log_timestamp": 1565023327.974799,           
 "file_name": "/var/projects/fynd/fynd-request-builder/src/fynd_request_builder/request.py",           
 "line_no": 217,           
 "function_name": "add_requests_logs",           
 "search_id": "f6699432-b79f-11e9-a13c-34415dc88eee",           
 "search_term": "aiohttp_request_trace_metric",           
 "action": "aiohttp_request_trace_metric",           
 "status": "success",           
 "payload": {"request_header": "[[\"X-Fynd-Trace-Id\",\"f6699432-b79f-11e9-a13c-34415dc88eee\"]]",       
			 "connect": 427.02,         
			 "transfer": 209.87,      
			 "total": 637.59,      
			 "is_redirect": false
			}
 }
 ```  
