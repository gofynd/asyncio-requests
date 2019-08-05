# Fynd Async HTTP Request Library
Used to make async http calls with inbuilt circuit breaker feature, uses aiohttp internally. 


### Work FLow
* Request are send to library, builds & performs checks on auth and headers and payloads provided.
* Since aiohttp is used to make http calls, event loop is used to make calls
* Circuit breaker checks are made before final request hit is done.
* Auto retry attempts are done by library if any network/OS exceptions or request time occurs
* Success/Fail/Exception Response will be provided to the client along with approprirate status code, message & response payload.

### How To Use
* Create instance of request builder library     
`request_builder = RequestBuilder()`     
* Design the http request payload as per below format     
`http_get_request_payload = {
   'url':'http://127.0.0.1:8001/store_search?productid=1,
   'verb':'GET',
   'cb_config':{
      'regex_pattern':'[1].+(?=/)'
   }
}`


* Make a call to `make_client_request`  with payload as argument    
`response = request_builder.make_client_request(http_get_request_payload)`


### Request format 
HTTP GET Request Format:  
```
{
   'url':'http://127.0.0.1:8001/store_search?productid=1,
   'verb':'GET',
   'cb_config':{
      'regex_pattern':'[1].+(?=/)'
   }
}
```
      
HTTP POST Request Format:    
```
{
   'url': 'https://reqres.in/api/users/1', 
   'verb': 'POST', 
   "data" : {"name":"morpheus","job":"leader"},
   'cb_config': {'regex_pattern': '[1].+(?=:)'}
   }
```

SOAP & XML Request Format:    
```
soap_xml='<soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:hs="http://www.holidaywebservice.com/HolidayService_v2/"><soapenv:Body><hs:GetHolidaysForMonth><hs:year>2019</hs:year><hs:countryCode>UnitedStates</hs:countryCode><hs:month>11</hs:month></hs:GetHolidaysForMonth></soapenv:Body></soapenv:Envelope>'
http_get_request_payload = {
   'url': 'http://www.holidaywebservice.com/HolidayService_v2/HolidayService2.asmx', 
   'verb': 'POST',
   'data':soap_xml,
   'cb_config': {'regex_pattern': ".*"},
   'headers':{'Content-Type':'text/xml'}, 
   'log_request_metric': 1
   }
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


###  Circuit Breaker (CB) Flow
* [WHAT is Circuit Breaker by. Martin Fowler.](https://martinfowler.com/bliki/CircuitBreaker.html)
* Whenever Network/OS or Request time out exception occurs for more than MAX auto retry attempts, circuit will open for particular request url.
* Client provided Regex is performed on requested url, this output is than used by CB to block all further calls to the same URI until cooling time elapses, current default cooling time is 10s
* Url is stored in Redis for default 10s,all re calls made to same URI are blocked by CB and actual http request is not done.
* After time elapses, URI is deleted from redis.
* Again if the same request is made from client, circuit is closed and attempt is made, if again exception occurs circuit is opend for 10s.
* `regex_pattern` is mandotory for each request,if missing/invalid full url path will be used by CB.
*  503 Service Unavailable , 504 Gateway Timeout, 509 Bandwidth Limit Exceeded (Apache), 429 Too Many Requests - Used by many API gateways for rate limiting - Are the list of status codes when auto retries triggers.



##### Current Supported HTTP Verbs
- GET
- POST
- PUT
- PATCH
- DELETE

#### Regex Pattern Examples
* We are using python re library [search()](https://docs.python.org/3/library/re.html#re.Pattern.search)  function to apply regex pattern to the string

 For Url : http://www.store1.com:8001/m_search?productId=11211

- `[w].+(?=/)` = `www.store1.com:8001`
- `[w].+(?=:)` = `www.store1.com`
- `.*` = `http://www.store1.com:8001/m_search?productId=11211`
- `.+m_` = `http://www.store1.com:8001/m_`

For Rest URLs : http://www.store1.com:8001/comment/postID/11211

- `[w].+(?=/)` = `www.store1.com:8001`
- `[w].+(?=)/` = `www.store1.com:8001/comment/postID/`
- `.*` = `http://www.store1.com:8001/m_search?productId=11211`

#### More :
* [aiohttp](https://aiohttp.readthedocs.io/en/stable/) is used to make async http calls
* [aopredis](https://aioredis.readthedocs.io/en/v1.2.0/index.html) is used to communicate with redis



