# gbs4api.ParameterDefControllerApi

All URIs are relative to *https://alfpwin0044.corp.passivesafety.com/gbs4-api*

Method | HTTP request | Description
------------- | ------------- | -------------
[**create_parameter_definition**](ParameterDefControllerApi.md#create_parameter_definition) | **POST** /api/v1/test-facilities/{testFacilityName}/parameter-definitions | 
[**delete_parameter_definition**](ParameterDefControllerApi.md#delete_parameter_definition) | **DELETE** /api/v1/test-facilities/{testFacilityName}/parameter-definitions/{parameterDefinitionName} | 
[**get_parameter_definitions_for_test_facility**](ParameterDefControllerApi.md#get_parameter_definitions_for_test_facility) | **GET** /api/v1/test-facilities/{testFacilityName}/parameter-definitions | 
[**update_parameter_definition**](ParameterDefControllerApi.md#update_parameter_definition) | **PUT** /api/v1/test-facilities/{testFacilityName}/parameter-definitions/{parameterDefinitionName} | 


# **create_parameter_definition**
> create_parameter_definition(test_facility_name, parameter_def_dto)

### Example


```python
import gbs4api
from gbs4api.models.parameter_def_dto import ParameterDefDto
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
    api_instance = gbs4api.ParameterDefControllerApi(api_client)
    test_facility_name = 'test_facility_name_example' # str | 
    parameter_def_dto = gbs4api.ParameterDefDto() # ParameterDefDto | 

    try:
        api_instance.create_parameter_definition(test_facility_name, parameter_def_dto)
    except Exception as e:
        print("Exception when calling ParameterDefControllerApi->create_parameter_definition: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **test_facility_name** | **str**|  | 
 **parameter_def_dto** | [**ParameterDefDto**](ParameterDefDto.md)|  | 

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

# **delete_parameter_definition**
> delete_parameter_definition(test_facility_name, parameter_definition_name)

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
    api_instance = gbs4api.ParameterDefControllerApi(api_client)
    test_facility_name = 'test_facility_name_example' # str | 
    parameter_definition_name = 'parameter_definition_name_example' # str | 

    try:
        api_instance.delete_parameter_definition(test_facility_name, parameter_definition_name)
    except Exception as e:
        print("Exception when calling ParameterDefControllerApi->delete_parameter_definition: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **test_facility_name** | **str**|  | 
 **parameter_definition_name** | **str**|  | 

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

# **get_parameter_definitions_for_test_facility**
> List[ParameterDefDto] get_parameter_definitions_for_test_facility(test_facility_name)

### Example


```python
import gbs4api
from gbs4api.models.parameter_def_dto import ParameterDefDto
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
    api_instance = gbs4api.ParameterDefControllerApi(api_client)
    test_facility_name = 'test_facility_name_example' # str | 

    try:
        api_response = api_instance.get_parameter_definitions_for_test_facility(test_facility_name)
        print("The response of ParameterDefControllerApi->get_parameter_definitions_for_test_facility:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling ParameterDefControllerApi->get_parameter_definitions_for_test_facility: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **test_facility_name** | **str**|  | 

### Return type

[**List[ParameterDefDto]**](ParameterDefDto.md)

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

# **update_parameter_definition**
> update_parameter_definition(test_facility_name, parameter_definition_name, parameter_def_dto)

### Example


```python
import gbs4api
from gbs4api.models.parameter_def_dto import ParameterDefDto
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
    api_instance = gbs4api.ParameterDefControllerApi(api_client)
    test_facility_name = 'test_facility_name_example' # str | 
    parameter_definition_name = 'parameter_definition_name_example' # str | 
    parameter_def_dto = gbs4api.ParameterDefDto() # ParameterDefDto | 

    try:
        api_instance.update_parameter_definition(test_facility_name, parameter_definition_name, parameter_def_dto)
    except Exception as e:
        print("Exception when calling ParameterDefControllerApi->update_parameter_definition: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **test_facility_name** | **str**|  | 
 **parameter_definition_name** | **str**|  | 
 **parameter_def_dto** | [**ParameterDefDto**](ParameterDefDto.md)|  | 

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

