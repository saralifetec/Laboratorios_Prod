# gbs4api.ValueListControllerApi

All URIs are relative to *https://alfpwin0044.corp.passivesafety.com/gbs4-api*

Method | HTTP request | Description
------------- | ------------- | -------------
[**get_value_lists**](ValueListControllerApi.md#get_value_lists) | **GET** /api/v1/value-lists/ | 
[**get_values_for_value_list**](ValueListControllerApi.md#get_values_for_value_list) | **GET** /api/v1/value-lists/{valueListname}/values | 


# **get_value_lists**
> List[ValueListDto] get_value_lists(name=name, string_matching_type=string_matching_type)

### Example


```python
import gbs4api
from gbs4api.models.value_list_dto import ValueListDto
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
    api_instance = gbs4api.ValueListControllerApi(api_client)
    name = 'name_example' # str |  (optional)
    string_matching_type = 'string_matching_type_example' # str |  (optional)

    try:
        api_response = api_instance.get_value_lists(name=name, string_matching_type=string_matching_type)
        print("The response of ValueListControllerApi->get_value_lists:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling ValueListControllerApi->get_value_lists: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **name** | **str**|  | [optional] 
 **string_matching_type** | **str**|  | [optional] 

### Return type

[**List[ValueListDto]**](ValueListDto.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: */*

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | OK |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_values_for_value_list**
> List[ValueDto] get_values_for_value_list(value_listname)

### Example


```python
import gbs4api
from gbs4api.models.value_dto import ValueDto
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
    api_instance = gbs4api.ValueListControllerApi(api_client)
    value_listname = 'value_listname_example' # str | 

    try:
        api_response = api_instance.get_values_for_value_list(value_listname)
        print("The response of ValueListControllerApi->get_values_for_value_list:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling ValueListControllerApi->get_values_for_value_list: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **value_listname** | **str**|  | 

### Return type

[**List[ValueDto]**](ValueDto.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: */*

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | OK |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

