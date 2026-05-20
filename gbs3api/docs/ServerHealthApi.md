# gbs3api.ServerHealthApi

All URIs are relative to */GBS*

Method | HTTP request | Description
------------- | ------------- | -------------
[**health**](ServerHealthApi.md#health) | **GET** /webservice/health | Displays some general information about the server such as version and instance
[**ping**](ServerHealthApi.md#ping) | **GET** /webservice/health/ping | Simply returns 200 OK with no body


# **health**
> str health()

Displays some general information about the server such as version and instance

### Example


```python
import gbs3api
from gbs3api.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to /GBS
# See configuration.py for a list of all supported configuration parameters.
configuration = gbs3api.Configuration(
    host = "/GBS"
)


# Enter a context with an instance of the API client
with gbs3api.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = gbs3api.ServerHealthApi(api_client)

    try:
        # Displays some general information about the server such as version and instance
        api_response = api_instance.health()
        print("The response of ServerHealthApi->health:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling ServerHealthApi->health: %s\n" % e)
```



### Parameters

This endpoint does not need any parameter.

### Return type

**str**

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | General server health information |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **ping**
> ping()

Simply returns 200 OK with no body

### Example


```python
import gbs3api
from gbs3api.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to /GBS
# See configuration.py for a list of all supported configuration parameters.
configuration = gbs3api.Configuration(
    host = "/GBS"
)


# Enter a context with an instance of the API client
with gbs3api.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = gbs3api.ServerHealthApi(api_client)

    try:
        # Simply returns 200 OK with no body
        api_instance.ping()
    except Exception as e:
        print("Exception when calling ServerHealthApi->ping: %s\n" % e)
```



### Parameters

This endpoint does not need any parameter.

### Return type

void (empty response body)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: Not defined

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Ping worked |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

