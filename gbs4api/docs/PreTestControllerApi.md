# gbs4api.PreTestControllerApi

All URIs are relative to *https://alfpwin0044.corp.passivesafety.com/gbs4-api*

Method | HTTP request | Description
------------- | ------------- | -------------
[**create_pre_test**](PreTestControllerApi.md#create_pre_test) | **POST** /api/v1/external-tests/{externalTestId}/pulses/{pulseTestCustomerRefNumber}/test-facilities/{testFacilityName}/pre-tests | 
[**create_pre_test_from_mme**](PreTestControllerApi.md#create_pre_test_from_mme) | **POST** /api/v1/external-tests/mme/{externalTestId}/pulses/{pulseTestCustomerRefNumber}/test-facilities/{testFacilityName}/pre-tests | 
[**delete_pre_test**](PreTestControllerApi.md#delete_pre_test) | **DELETE** /api/v1/external-tests/{externalTestId}/pulses/{pulseTestCustomerRefNumber}/test-facilities/{testFacilityName}/pre-tests/{preTestCustomerRefNumber} | 
[**get_pre_tests**](PreTestControllerApi.md#get_pre_tests) | **GET** /api/v1/external-tests/{externalTestId}/pulses/{pulseTestCustomerRefNumber}/test-facilities/{testFacilityName}/pre-tests | 
[**update_pre_test**](PreTestControllerApi.md#update_pre_test) | **PUT** /api/v1/external-tests/{externalTestId}/pulses/{pulseTestCustomerRefNumber}/test-facilities/{testFacilityName}/pre-tests/{preTestCustomerRefNumber} | 
[**upload_report_for_pre_test**](PreTestControllerApi.md#upload_report_for_pre_test) | **PUT** /api/v1/external-tests/{externalTestId}/pulse-tests/{pulseTestCustomerRefNumber}/test-facilities/{testFacilityName}/pre-tests/{preTestCustomerRefNumber}/pdf | 


# **create_pre_test**
> create_pre_test(external_test_id, pulse_test_customer_ref_number, test_facility_name, pre_test_dto)

### Example


```python
import gbs4api
from gbs4api.models.pre_test_dto import PreTestDto
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
    api_instance = gbs4api.PreTestControllerApi(api_client)
    external_test_id = 'external_test_id_example' # str | 
    pulse_test_customer_ref_number = 'pulse_test_customer_ref_number_example' # str | 
    test_facility_name = 'test_facility_name_example' # str | 
    pre_test_dto = gbs4api.PreTestDto() # PreTestDto | 

    try:
        api_instance.create_pre_test(external_test_id, pulse_test_customer_ref_number, test_facility_name, pre_test_dto)
    except Exception as e:
        print("Exception when calling PreTestControllerApi->create_pre_test: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **external_test_id** | **str**|  | 
 **pulse_test_customer_ref_number** | **str**|  | 
 **test_facility_name** | **str**|  | 
 **pre_test_dto** | [**PreTestDto**](PreTestDto.md)|  | 

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

# **create_pre_test_from_mme**
> PreTestDto create_pre_test_from_mme(external_test_id, pulse_test_customer_ref_number, test_facility_name, files=files)

### Example


```python
import gbs4api
from gbs4api.models.pre_test_dto import PreTestDto
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
    api_instance = gbs4api.PreTestControllerApi(api_client)
    external_test_id = 'external_test_id_example' # str | 
    pulse_test_customer_ref_number = 'pulse_test_customer_ref_number_example' # str | 
    test_facility_name = 'test_facility_name_example' # str | 
    files = None # List[bytes] |  (optional)

    try:
        api_response = api_instance.create_pre_test_from_mme(external_test_id, pulse_test_customer_ref_number, test_facility_name, files=files)
        print("The response of PreTestControllerApi->create_pre_test_from_mme:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling PreTestControllerApi->create_pre_test_from_mme: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **external_test_id** | **str**|  | 
 **pulse_test_customer_ref_number** | **str**|  | 
 **test_facility_name** | **str**|  | 
 **files** | **List[bytes]**|  | [optional] 

### Return type

[**PreTestDto**](PreTestDto.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: multipart/form-data
 - **Accept**: */*

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**201** | Created |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **delete_pre_test**
> delete_pre_test(external_test_id, pulse_test_customer_ref_number, test_facility_name, pre_test_customer_ref_number)

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
    api_instance = gbs4api.PreTestControllerApi(api_client)
    external_test_id = 'external_test_id_example' # str | 
    pulse_test_customer_ref_number = 'pulse_test_customer_ref_number_example' # str | 
    test_facility_name = 'test_facility_name_example' # str | 
    pre_test_customer_ref_number = 'pre_test_customer_ref_number_example' # str | 

    try:
        api_instance.delete_pre_test(external_test_id, pulse_test_customer_ref_number, test_facility_name, pre_test_customer_ref_number)
    except Exception as e:
        print("Exception when calling PreTestControllerApi->delete_pre_test: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **external_test_id** | **str**|  | 
 **pulse_test_customer_ref_number** | **str**|  | 
 **test_facility_name** | **str**|  | 
 **pre_test_customer_ref_number** | **str**|  | 

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

# **get_pre_tests**
> List[PreTestDto] get_pre_tests(external_test_id, pulse_test_customer_ref_number, test_facility_name)

### Example


```python
import gbs4api
from gbs4api.models.pre_test_dto import PreTestDto
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
    api_instance = gbs4api.PreTestControllerApi(api_client)
    external_test_id = 'external_test_id_example' # str | 
    pulse_test_customer_ref_number = 'pulse_test_customer_ref_number_example' # str | 
    test_facility_name = 'test_facility_name_example' # str | 

    try:
        api_response = api_instance.get_pre_tests(external_test_id, pulse_test_customer_ref_number, test_facility_name)
        print("The response of PreTestControllerApi->get_pre_tests:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling PreTestControllerApi->get_pre_tests: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **external_test_id** | **str**|  | 
 **pulse_test_customer_ref_number** | **str**|  | 
 **test_facility_name** | **str**|  | 

### Return type

[**List[PreTestDto]**](PreTestDto.md)

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

# **update_pre_test**
> update_pre_test(external_test_id, pulse_test_customer_ref_number, test_facility_name, pre_test_customer_ref_number, pre_test_dto)

### Example


```python
import gbs4api
from gbs4api.models.pre_test_dto import PreTestDto
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
    api_instance = gbs4api.PreTestControllerApi(api_client)
    external_test_id = 'external_test_id_example' # str | 
    pulse_test_customer_ref_number = 'pulse_test_customer_ref_number_example' # str | 
    test_facility_name = 'test_facility_name_example' # str | 
    pre_test_customer_ref_number = 'pre_test_customer_ref_number_example' # str | 
    pre_test_dto = gbs4api.PreTestDto() # PreTestDto | 

    try:
        api_instance.update_pre_test(external_test_id, pulse_test_customer_ref_number, test_facility_name, pre_test_customer_ref_number, pre_test_dto)
    except Exception as e:
        print("Exception when calling PreTestControllerApi->update_pre_test: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **external_test_id** | **str**|  | 
 **pulse_test_customer_ref_number** | **str**|  | 
 **test_facility_name** | **str**|  | 
 **pre_test_customer_ref_number** | **str**|  | 
 **pre_test_dto** | [**PreTestDto**](PreTestDto.md)|  | 

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

# **upload_report_for_pre_test**
> str upload_report_for_pre_test(external_test_id, pulse_test_customer_ref_number, test_facility_name, pre_test_customer_ref_number, file)

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
    api_instance = gbs4api.PreTestControllerApi(api_client)
    external_test_id = 'external_test_id_example' # str | 
    pulse_test_customer_ref_number = 'pulse_test_customer_ref_number_example' # str | 
    test_facility_name = 'test_facility_name_example' # str | 
    pre_test_customer_ref_number = 'pre_test_customer_ref_number_example' # str | 
    file = None # bytes | 

    try:
        api_response = api_instance.upload_report_for_pre_test(external_test_id, pulse_test_customer_ref_number, test_facility_name, pre_test_customer_ref_number, file)
        print("The response of PreTestControllerApi->upload_report_for_pre_test:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling PreTestControllerApi->upload_report_for_pre_test: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **external_test_id** | **str**|  | 
 **pulse_test_customer_ref_number** | **str**|  | 
 **test_facility_name** | **str**|  | 
 **pre_test_customer_ref_number** | **str**|  | 
 **file** | **bytes**|  | 

### Return type

**str**

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: multipart/form-data
 - **Accept**: */*

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | OK |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

