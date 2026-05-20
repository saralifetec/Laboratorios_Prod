# gbs4api.ParameterValueControllerApi

All URIs are relative to *https://alfpwin0044.corp.passivesafety.com/gbs4-api*

Method | HTTP request | Description
------------- | ------------- | -------------
[**get_parameters**](ParameterValueControllerApi.md#get_parameters) | **GET** /api/v1/external-tests/{externalTestId}/pulses/{pulseTestCustomerRef}/test-facilities/{testFacilityName}/pre-tests/{preTestCustomerRef}/parameters | 
[**update_parameters**](ParameterValueControllerApi.md#update_parameters) | **PUT** /api/v1/external-tests/{externalTestId}/pulses/{pulseTestCustomerRef}/test-facilities/{testFacilityName}/pre-tests/{preTestCustomerRef}/parameters/{parameterName} | 


# **get_parameters**
> List[ParameterValueDto] get_parameters(external_test_id, pulse_test_customer_ref, test_facility_name, pre_test_customer_ref)

### Example


```python
import gbs4api
from gbs4api.models.parameter_value_dto import ParameterValueDto
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
    api_instance = gbs4api.ParameterValueControllerApi(api_client)
    external_test_id = 'external_test_id_example' # str | 
    pulse_test_customer_ref = 'pulse_test_customer_ref_example' # str | 
    test_facility_name = 'test_facility_name_example' # str | 
    pre_test_customer_ref = 'pre_test_customer_ref_example' # str | 

    try:
        api_response = api_instance.get_parameters(external_test_id, pulse_test_customer_ref, test_facility_name, pre_test_customer_ref)
        print("The response of ParameterValueControllerApi->get_parameters:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling ParameterValueControllerApi->get_parameters: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **external_test_id** | **str**|  | 
 **pulse_test_customer_ref** | **str**|  | 
 **test_facility_name** | **str**|  | 
 **pre_test_customer_ref** | **str**|  | 

### Return type

[**List[ParameterValueDto]**](ParameterValueDto.md)

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

# **update_parameters**
> update_parameters(external_test_id, pulse_test_customer_ref, test_facility_name, pre_test_customer_ref, parameter_name, value)

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
    api_instance = gbs4api.ParameterValueControllerApi(api_client)
    external_test_id = 'external_test_id_example' # str | 
    pulse_test_customer_ref = 'pulse_test_customer_ref_example' # str | 
    test_facility_name = 'test_facility_name_example' # str | 
    pre_test_customer_ref = 'pre_test_customer_ref_example' # str | 
    parameter_name = 'parameter_name_example' # str | 
    value = 'value_example' # str | 

    try:
        api_instance.update_parameters(external_test_id, pulse_test_customer_ref, test_facility_name, pre_test_customer_ref, parameter_name, value)
    except Exception as e:
        print("Exception when calling ParameterValueControllerApi->update_parameters: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **external_test_id** | **str**|  | 
 **pulse_test_customer_ref** | **str**|  | 
 **test_facility_name** | **str**|  | 
 **pre_test_customer_ref** | **str**|  | 
 **parameter_name** | **str**|  | 
 **value** | **str**|  | 

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

