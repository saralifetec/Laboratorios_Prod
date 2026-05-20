# gbs3api.DeviceApi

All URIs are relative to */GBS*

Method | HTTP request | Description
------------- | ------------- | -------------
[**remind**](DeviceApi.md#remind) | **POST** /webservice/device/remind | 


# **remind**
> remind(rental_id=rental_id)

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
    api_instance = gbs3api.DeviceApi(api_client)
    rental_id = 'rental_id_example' # str |  (optional)

    try:
        api_instance.remind(rental_id=rental_id)
    except Exception as e:
        print("Exception when calling DeviceApi->remind: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **rental_id** | **str**|  | [optional] 

### Return type

void (empty response body)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: */*

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**0** | default response |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

