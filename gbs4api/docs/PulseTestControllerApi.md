# gbs4api.PulseTestControllerApi

All URIs are relative to *https://alfpwin0044.corp.passivesafety.com/gbs4-api*

Method | HTTP request | Description
------------- | ------------- | -------------
[**create_pulse_test**](PulseTestControllerApi.md#create_pulse_test) | **POST** /api/v1/external-tests/{externalTestId}/pulses | 
[**create_pulse_test_from_mme**](PulseTestControllerApi.md#create_pulse_test_from_mme) | **POST** /api/v1/external-tests/mme/{externalTestId}/pulses | 
[**delete_pulse_test**](PulseTestControllerApi.md#delete_pulse_test) | **DELETE** /api/v1/external-tests/{externalTestId}/pulses/{pulseTestCustomerRefNumber} | 
[**get_all_test_facility_from_pulse_tests**](PulseTestControllerApi.md#get_all_test_facility_from_pulse_tests) | **GET** /api/v1/external-tests/{externalTestId}/pulses/{pulseTestCustomerRefNumber}/test-facilities | 
[**get_pulse_test_for_external_test**](PulseTestControllerApi.md#get_pulse_test_for_external_test) | **GET** /api/v1/external-tests/{externalTestId}/pulses/{pulseTestCustomerRefNumber} | 
[**get_pulse_tests_for_external_test**](PulseTestControllerApi.md#get_pulse_tests_for_external_test) | **GET** /api/v1/external-tests/{externalTestId}/pulses | 
[**update_pulse_test**](PulseTestControllerApi.md#update_pulse_test) | **PUT** /api/v1/external-tests/{externalTestId}/pulses/{pulseTestCustomerRefNumber} | 
[**update_pulse_test_from_mme**](PulseTestControllerApi.md#update_pulse_test_from_mme) | **PUT** /api/v1/external-tests/mme/{externalTestId}/pulses/{pulseTestCustomerRefNumber} | 
[**upload_report_for_pulse_test**](PulseTestControllerApi.md#upload_report_for_pulse_test) | **PUT** /api/v1/external-tests/{externalTestId}/pulse-tests/{pulseTestCustomerRefNumber}/pdf | 


# **create_pulse_test**
> create_pulse_test(external_test_id, pulse_test_dto)

### Example


```python
import gbs4api
from gbs4api.models.pulse_test_dto import PulseTestDto
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
    api_instance = gbs4api.PulseTestControllerApi(api_client)
    external_test_id = 'external_test_id_example' # str | 
    pulse_test_dto = gbs4api.PulseTestDto() # PulseTestDto | 

    try:
        api_instance.create_pulse_test(external_test_id, pulse_test_dto)
    except Exception as e:
        print("Exception when calling PulseTestControllerApi->create_pulse_test: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **external_test_id** | **str**|  | 
 **pulse_test_dto** | [**PulseTestDto**](PulseTestDto.md)|  | 

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

# **create_pulse_test_from_mme**
> PulseTestDto create_pulse_test_from_mme(external_test_id, files=files)

### Example


```python
import gbs4api
from gbs4api.models.pulse_test_dto import PulseTestDto
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
    api_instance = gbs4api.PulseTestControllerApi(api_client)
    external_test_id = 'external_test_id_example' # str | 
    files = None # List[bytes] |  (optional)

    try:
        api_response = api_instance.create_pulse_test_from_mme(external_test_id, files=files)
        print("The response of PulseTestControllerApi->create_pulse_test_from_mme:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling PulseTestControllerApi->create_pulse_test_from_mme: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **external_test_id** | **str**|  | 
 **files** | **List[bytes]**|  | [optional] 

### Return type

[**PulseTestDto**](PulseTestDto.md)

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

# **delete_pulse_test**
> delete_pulse_test(external_test_id, pulse_test_customer_ref_number)

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
    api_instance = gbs4api.PulseTestControllerApi(api_client)
    external_test_id = 'external_test_id_example' # str | 
    pulse_test_customer_ref_number = 'pulse_test_customer_ref_number_example' # str | 

    try:
        api_instance.delete_pulse_test(external_test_id, pulse_test_customer_ref_number)
    except Exception as e:
        print("Exception when calling PulseTestControllerApi->delete_pulse_test: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **external_test_id** | **str**|  | 
 **pulse_test_customer_ref_number** | **str**|  | 

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

# **get_all_test_facility_from_pulse_tests**
> List[TestFacilityDto] get_all_test_facility_from_pulse_tests(external_test_id, pulse_test_customer_ref_number)

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
    api_instance = gbs4api.PulseTestControllerApi(api_client)
    external_test_id = 'external_test_id_example' # str | 
    pulse_test_customer_ref_number = 'pulse_test_customer_ref_number_example' # str | 

    try:
        api_response = api_instance.get_all_test_facility_from_pulse_tests(external_test_id, pulse_test_customer_ref_number)
        print("The response of PulseTestControllerApi->get_all_test_facility_from_pulse_tests:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling PulseTestControllerApi->get_all_test_facility_from_pulse_tests: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **external_test_id** | **str**|  | 
 **pulse_test_customer_ref_number** | **str**|  | 

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

# **get_pulse_test_for_external_test**
> PulseTestDto get_pulse_test_for_external_test(external_test_id, pulse_test_customer_ref_number)

### Example


```python
import gbs4api
from gbs4api.models.pulse_test_dto import PulseTestDto
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
    api_instance = gbs4api.PulseTestControllerApi(api_client)
    external_test_id = 'external_test_id_example' # str | 
    pulse_test_customer_ref_number = 'pulse_test_customer_ref_number_example' # str | 

    try:
        api_response = api_instance.get_pulse_test_for_external_test(external_test_id, pulse_test_customer_ref_number)
        print("The response of PulseTestControllerApi->get_pulse_test_for_external_test:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling PulseTestControllerApi->get_pulse_test_for_external_test: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **external_test_id** | **str**|  | 
 **pulse_test_customer_ref_number** | **str**|  | 

### Return type

[**PulseTestDto**](PulseTestDto.md)

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

# **get_pulse_tests_for_external_test**
> List[PulseTestDto] get_pulse_tests_for_external_test(external_test_id)

### Example


```python
import gbs4api
from gbs4api.models.pulse_test_dto import PulseTestDto
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
    api_instance = gbs4api.PulseTestControllerApi(api_client)
    external_test_id = 'external_test_id_example' # str | 

    try:
        api_response = api_instance.get_pulse_tests_for_external_test(external_test_id)
        print("The response of PulseTestControllerApi->get_pulse_tests_for_external_test:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling PulseTestControllerApi->get_pulse_tests_for_external_test: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **external_test_id** | **str**|  | 

### Return type

[**List[PulseTestDto]**](PulseTestDto.md)

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

# **update_pulse_test**
> update_pulse_test(external_test_id, pulse_test_customer_ref_number, pulse_test_dto)

### Example


```python
import gbs4api
from gbs4api.models.pulse_test_dto import PulseTestDto
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
    api_instance = gbs4api.PulseTestControllerApi(api_client)
    external_test_id = 'external_test_id_example' # str | 
    pulse_test_customer_ref_number = 'pulse_test_customer_ref_number_example' # str | 
    pulse_test_dto = gbs4api.PulseTestDto() # PulseTestDto | 

    try:
        api_instance.update_pulse_test(external_test_id, pulse_test_customer_ref_number, pulse_test_dto)
    except Exception as e:
        print("Exception when calling PulseTestControllerApi->update_pulse_test: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **external_test_id** | **str**|  | 
 **pulse_test_customer_ref_number** | **str**|  | 
 **pulse_test_dto** | [**PulseTestDto**](PulseTestDto.md)|  | 

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

# **update_pulse_test_from_mme**
> PulseTestDto update_pulse_test_from_mme(external_test_id, pulse_test_customer_ref_number, force, files=files)

### Example


```python
import gbs4api
from gbs4api.models.pulse_test_dto import PulseTestDto
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
    api_instance = gbs4api.PulseTestControllerApi(api_client)
    external_test_id = 'external_test_id_example' # str | 
    pulse_test_customer_ref_number = 'pulse_test_customer_ref_number_example' # str | 
    force = True # bool | 
    files = None # List[bytes] |  (optional)

    try:
        api_response = api_instance.update_pulse_test_from_mme(external_test_id, pulse_test_customer_ref_number, force, files=files)
        print("The response of PulseTestControllerApi->update_pulse_test_from_mme:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling PulseTestControllerApi->update_pulse_test_from_mme: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **external_test_id** | **str**|  | 
 **pulse_test_customer_ref_number** | **str**|  | 
 **force** | **bool**|  | 
 **files** | **List[bytes]**|  | [optional] 

### Return type

[**PulseTestDto**](PulseTestDto.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: multipart/form-data
 - **Accept**: */*

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**204** | No Content |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **upload_report_for_pulse_test**
> str upload_report_for_pulse_test(external_test_id, pulse_test_customer_ref_number, file)

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
    api_instance = gbs4api.PulseTestControllerApi(api_client)
    external_test_id = 'external_test_id_example' # str | 
    pulse_test_customer_ref_number = 'pulse_test_customer_ref_number_example' # str | 
    file = None # bytes | 

    try:
        api_response = api_instance.upload_report_for_pulse_test(external_test_id, pulse_test_customer_ref_number, file)
        print("The response of PulseTestControllerApi->upload_report_for_pulse_test:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling PulseTestControllerApi->upload_report_for_pulse_test: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **external_test_id** | **str**|  | 
 **pulse_test_customer_ref_number** | **str**|  | 
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

