# FDK Python

![GitHub requirements.txt version](https://img.shields.io/github/package-json/v/gofynd/fdk-client-python?style=plastic)
![GitHub Workflow Status](https://img.shields.io/github/workflow/status/gofynd/fdk-client-python?style=plastic)
![GitHub](https://img.shields.io/github/license/gofynd/fdk-client-python?style=plastic)
[![Coverage Status](https://coveralls.io/repos/github/gofynd/fdk-client-python/badge.svg)](https://coveralls.io/github/gofynd/fdk-client-python)

FDK client for python

## Getting Started

Get started with the python Development SDK for Fynd Platform

### Usage

```
pip install fdk-client-python
```

Using this method, you can `import` fdk-client-python like so:

```python
from fdk_client_python.sdk.application.ApplicationClient import ApplicationClient
from fdk_client_python.sdk.application.ApplicationConfig import ApplicationConfig
```

### Sample Usage - ApplicationClient

```python
config = ApplicationConfig({
    "applicationID": "YOUR_APPLICATION_ID",
    "applicationToken": "YOUR_APPLICATION_TOKEN",
    "domain": "YOUR_DOMAIN"
})

applicationClient = ApplicationClient(config)

async def getProductDetails():
    try:
        product = await applicationClient.catalog.getProductDetailBySlug(slug="product-slug")
        print(product)
    except Exception as e:
        print(e)

getProductDetails()
```

### Sample Usage - PlatformClient


```python
from fdk_client_python.sdk.common.aiohttp_helper import AiohttpHelper
from fdk_client_python.sdk.platform.PlatformConfig import PlatformConfig
from fdk_client_python.sdk.platform.PlatformClient import PlatformClient
from fdk_client_python.sdk.common.utils import create_url_without_domain, get_headers_with_signature


async def setAccessToken(platformConfig, cookies):
    reqData = {
        "grant_type": "client_credentials",
        "client_id": platformConfig.apiKey,
        "client_secret": platformConfig.apiSecret
    }
    url = f"{platformConfig.domain}/service/panel/authentication/v1.0/company/{platformConfig.companyId}/oauth/token"
    url_without_domain = await create_url_without_domain(f"/service/panel/authentication/v1.0/company/{platformConfig.companyId}/oauth/token")
    headers = await get_headers_with_signature(platformConfig.domain, "post", url_without_domain, "", {}, reqData)
    res = await AiohttpHelper().aiohttp_request("POST", url, reqData, headers, cookies=cookies)
    return res["json"]

async def loginUser(platformConfig):
    skywarpURL = f"{platformConfig.domain}/service/panel/authentication/v1.0/auth/login/password"
    userData = {
        "username": "YOUR_USERNAME",
        "password": "YOUR_PASSWORD",
        "g-recaptcha-response": "_skip_"
    }
    url_without_domain = "/service/panel/authentication/v1.0/auth/login/password"
    headers = await get_headers_with_signature(platformConfig.domain, "post", url_without_domain, "", {}, userData)
    res = await AiohttpHelper().aiohttp_request("POST", skywarpURL, userData, headers)
    return res

try:
    platformConfig = PlatformConfig({
        "companyId": "YOUR_COMPANY_ID",
        "domain": "YOUR_DOMAIN",
        "apiKey": "YOUR_APIKEY",
        "apiSecret": "YOUR_APISECRET"
    })
    loginResponse = await loginUser(platformConfig)
    # print(loginResponse)
    tokenResponse = await setAccessToken(platformConfig, loginResponse["cookies"])
    # print(tokenResponse)
    await platformConfig.oauthClient.setToken(tokenResponse)
    platformClient = PlatformClient(platformConfig)
    res = await platformClient.lead.getTicket(id="YOUR_TICKET_ID")
    # use res
except Exception as e:
    print(e)
```