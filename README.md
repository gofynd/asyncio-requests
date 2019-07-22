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
   'url':'http://127.0.0.1:8001/store_search?actor='   +str(icount),
   'verb':'GET',
   'cb_config':{
      'regex_pattern':'[1].+(?=/)'
   }
}
POST HTTP Request 
{
   'url':'http://127.0.0.1:8001/store_add',
   'verb':'POST',
   'data':{
      "name":"Kaushil"
   },
   'cb_config':{
      'regex_pattern':'[1].+(?=:)'
   }
} 



###  Client Usage
##### Getting Started
Install the package   
`PIP install FyndLogger ` 

Import the module  
`from fynd_logger import FyndLogger`

Call the logging API methods as follows with your message as arguments  
`FyndLogger.info("This is info to log")`

```python
def bag_assign_dp():
    dp_assign_failure_message = "Failed to assign dp for bag id : 500005"
    FyndLogger.action(dp_assign_failure_message)
```


Currently it supports following log methods  
`critical(),error(),warning(),info(),debug()`

For action logs   


```python
def calculate_store_distance():
    shipment_log = { 
    "search_id": AWB-12092019-93,   
    "search_term": "store_location",   
    "action": "calculate_store_distance",    
    "status": "success",      
    "payload": {}
    }   
    FyndLogger.action(shipment_log)
```

### Benefits over current Inbult Logging API
* This will be the single library used across org, which maintains uniformity.  
* Feature addition or changes will help reflect across project.
* It also provides deatiled information related to File,Function and Line number from where the log was generated.
* Action() method can log different events,actions with json payload.
* All the action-logs JSON key-value pairs will be mapped to indexed in ELK and will be searchable. 
* Action logs will be helpful for debugging, verifying data journery,tarce and pinpointing failure in code.
* For ELK search SS and detail doc refer [Fynd-Logger]([https://gofynd.quip.com/WDZKAWndNLaP/Fynd-Logger])



