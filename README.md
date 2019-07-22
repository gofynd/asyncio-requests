# Fynd Async HTTP Request Library
Used to make async http calls with inbuilt circuit breaker feature, uses aiohttp internally. 


### Work FLow
* Request are send to library, builds & performs checks on auth and headers and payloads provided.
* Since aiohttp is used to make http calls, event loop is used to make calls
* Circuit breaker checks are made before final request hit is done.
* Auto retry attempts are done by library if any network/OS exceptions or request time occurs
* Success/Fail/Exception Response will be provided to the client along with approprirate status code, message & response payload.

### Request format 
GET HTTP Request Format   
`{
   'url':'http://127.0.0.1:8001/store_search?productid=1,
   'verb':'GET',
   'cb_config':{
      'regex_pattern':'[1].+(?=/)'
   }
}`
      

POST HTTP Request Format    
`{
   'url':'http://127.0.0.1:8001/store_add',
   'verb':'POST',
   'data':{
      "name":"Kaushil"
   },
   'cb_config':{
      'regex_pattern':''
   }
}`



###  Circuit Breaker (CB) Flow
* Whenever Network/OS or Request time out exception occurs for more than MAX auto retry times, circuit will open for particular request url.
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
* We are using python re library `search()` function to apply regex pattern to the string

 For Url : http://www.store1.com:8001/m_search?productId=11211

- `[w].+(?=/)` = `www.store1.com:8001`
- `[w].+(?=:)` = `www.store1.com`
- `.*` = `http://www.store1.com:8001/m_search?productId=11211`
- `.+m_` = `http://www.store1.com:8001/m_`

For Rest URLs : http://www.store1.com:8001/comment/postID/11211

- `[w].+(?=/)` = `www.store1.com:8001`
- `[w].+(?=)/` = `www.store1.com:8001/comment/postID/`
- `.*` = `http://www.store1.com:8001/m_search?productId=11211`



### Benefits over current Inbult Logging API
* This will be the single library used across org, which maintains uniformity.  
* Feature addition or changes will help reflect across project.
* It also provides deatiled information related to File,Function and Line number from where the log was generated.
* Action() method can log different events,actions with json payload.
* All the action-logs JSON key-value pairs will be mapped to indexed in ELK and will be searchable. 
* Action logs will be helpful for debugging, verifying data journery,tarce and pinpointing failure in code.
* For ELK search SS and detail doc refer [Fynd-Logger]([https://gofynd.quip.com/WDZKAWndNLaP/Fynd-Logger])



