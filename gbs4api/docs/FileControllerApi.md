# gbs4api.FileControllerApi

All URIs are relative to *https://alfpwin0044.corp.passivesafety.com/gbs4-api*

Method | HTTP request | Description
------------- | ------------- | -------------
[**get_file**](FileControllerApi.md#get_file) | **GET** /api/v1/files/{id} | Download a file


# **get_file**
> bytes get_file(id, download=download)

Download a file

Returns a file as a binary stream

### Example


```python
import gbs4api
from gbs4api.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to https://alfpwin0044.corp.passivesafety.com/gbs4-api
# See configuration.py for a list of all supported configuration parameters.
configuration = gbs4api.Configuration(
    host = "https://alfpwin0044.corp.passivesafety.com/gbs4-api"
)


# Enter a context with an instance of the API client
with gbs4api.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = gbs4api.FileControllerApi(api_client)
    id = 56 # int | 
    download = False # bool |  (optional) (default to False)

    try:
        # Download a file
        api_response = api_instance.get_file(id, download=download)
        print("The response of FileControllerApi->get_file:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling FileControllerApi->get_file: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **int**|  | 
 **download** | **bool**|  | [optional] [default to False]

### Return type

**bytes**

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/octet-stream

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | File downloaded successfully |  -  |
**404** | File not found |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

