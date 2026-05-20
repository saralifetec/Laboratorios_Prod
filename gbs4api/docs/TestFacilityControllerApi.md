# gbs4api.TestFacilityControllerApi

All URIs are relative to *https://alfpwin0044.corp.passivesafety.com/gbs4-api*

Method | HTTP request | Description
------------- | ------------- | -------------
[**create_test_facility**](TestFacilityControllerApi.md#create_test_facility) | **POST** /api/v1/test-facilities | 
[**delete_test_facility**](TestFacilityControllerApi.md#delete_test_facility) | **DELETE** /api/v1/test-facilities/{testFacilityName} | 
[**get_test_facilities**](TestFacilityControllerApi.md#get_test_facilities) | **GET** /api/v1/test-facilities | 
[**get_test_facility**](TestFacilityControllerApi.md#get_test_facility) | **GET** /api/v1/test-facilities/{testFacilityName} | 
[**update_test_facility**](TestFacilityControllerApi.md#update_test_facility) | **PUT** /api/v1/test-facilities/{testFacilityName} | 


# **create_test_facility**
> create_test_facility(test_facility_dto)

### Example


```python
import gbs4api
from gbs4api.models.test_facility_dto import TestFacilityDto
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
    api_instance = gbs4api.TestFacilityControllerApi(api_client)
    test_facility_dto = gbs4api.TestFacilityDto() # TestFacilityDto | 

    try:
        api_instance.create_test_facility(test_facility_dto)
    except Exception as e:
        print("Exception when calling TestFacilityControllerApi->create_test_facility: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **test_facility_dto** | [**TestFacilityDto**](TestFacilityDto.md)|  | 

### Return type

void (empty response body)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: Not defined

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**201** | Created |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **delete_test_facility**
> delete_test_facility(test_facility_name)

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
    api_instance = gbs4api.TestFacilityControllerApi(api_client)
    test_facility_name = 'test_facility_name_example' # str | 

    try:
        api_instance.delete_test_facility(test_facility_name)
    except Exception as e:
        print("Exception when calling TestFacilityControllerApi->delete_test_facility: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **test_facility_name** | **str**|  | 

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
**204** | No Content |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_test_facilities**
> List[TestFacilityDto] get_test_facilities()

### Example


```python
import gbs4api
from gbs4api.models.test_facility_dto import TestFacilityDto
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
    api_instance = gbs4api.TestFacilityControllerApi(api_client)

    try:
        api_response = api_instance.get_test_facilities()
        print("The response of TestFacilityControllerApi->get_test_facilities:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling TestFacilityControllerApi->get_test_facilities: %s\n" % e)
```



### Parameters

This endpoint does not need any parameter.

### Return type

[**List[TestFacilityDto]**](TestFacilityDto.md)

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

# **get_test_facility**
> TestFacilityDto get_test_facility(test_facility_name)

### Example


```python
import gbs4api
from gbs4api.models.test_facility_dto import TestFacilityDto
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
    api_instance = gbs4api.TestFacilityControllerApi(api_client)
    test_facility_name = 'test_facility_name_example' # str | 

    try:
        api_response = api_instance.get_test_facility(test_facility_name)
        print("The response of TestFacilityControllerApi->get_test_facility:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling TestFacilityControllerApi->get_test_facility: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **test_facility_name** | **str**|  | 

### Return type

[**TestFacilityDto**](TestFacilityDto.md)

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

# **update_test_facility**
> update_test_facility(test_facility_name, test_facility_dto)

### Example


```python
import gbs4api
from gbs4api.models.test_facility_dto import TestFacilityDto
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
    api_instance = gbs4api.TestFacilityControllerApi(api_client)
    test_facility_name = 'test_facility_name_example' # str | 
    test_facility_dto = gbs4api.TestFacilityDto() # TestFacilityDto | 

    try:
        api_instance.update_test_facility(test_facility_name, test_facility_dto)
    except Exception as e:
        print("Exception when calling TestFacilityControllerApi->update_test_facility: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **test_facility_name** | **str**|  | 
 **test_facility_dto** | [**TestFacilityDto**](TestFacilityDto.md)|  | 

### Return type

void (empty response body)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: Not defined

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**204** | No Content |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

