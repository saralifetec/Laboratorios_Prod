# gbs4api.CommentControllerApi

All URIs are relative to *https://alfpwin0044.corp.passivesafety.com/gbs4-api*

Method | HTTP request | Description
------------- | ------------- | -------------
[**create_comment_for_external_test**](CommentControllerApi.md#create_comment_for_external_test) | **POST** /api/v1/external-tests/{externalTestId}/comments | 
[**create_comment_for_pre_test**](CommentControllerApi.md#create_comment_for_pre_test) | **POST** /api/v1/external-tests/{externalTestId}/pulses/{pulseTestCustomerRefNumber}/test-facilities/{testFacilityName}/pre-tests/{preTestCustomerRefNumber}/comments | 
[**create_comment_for_pulse_test**](CommentControllerApi.md#create_comment_for_pulse_test) | **POST** /api/v1/external-tests/{externalTestId}/pulses/{pulseTestCustomerRefNumber}/comments | 
[**get_comments_for_external_test**](CommentControllerApi.md#get_comments_for_external_test) | **GET** /api/v1/external-tests/{externalTestId}/comments | 
[**get_comments_for_pre_test**](CommentControllerApi.md#get_comments_for_pre_test) | **GET** /api/v1/external-tests/{externalTestId}/pulses/{pulseTestCustomerRefNumber}/test-facilities/{testFacilityName}/pre-tests/{preTestCustomerRefNumber}/comments | 
[**get_comments_for_pulse_test**](CommentControllerApi.md#get_comments_for_pulse_test) | **GET** /api/v1/external-tests/{externalTestId}/pulses/{pulseTestCustomerRefNumber}/comments | 


# **create_comment_for_external_test**
> CommentDto create_comment_for_external_test(external_test_id, body)

### Example


```python
import gbs4api
from gbs4api.models.comment_dto import CommentDto
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
    api_instance = gbs4api.CommentControllerApi(api_client)
    external_test_id = 'external_test_id_example' # str | 
    body = 'body_example' # str | 

    try:
        api_response = api_instance.create_comment_for_external_test(external_test_id, body)
        print("The response of CommentControllerApi->create_comment_for_external_test:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling CommentControllerApi->create_comment_for_external_test: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **external_test_id** | **str**|  | 
 **body** | **str**|  | 

### Return type

[**CommentDto**](CommentDto.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: text/plain
 - **Accept**: */*

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**201** | Created |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **create_comment_for_pre_test**
> CommentDto create_comment_for_pre_test(external_test_id, pulse_test_customer_ref_number, test_facility_name, pre_test_customer_ref_number, body)

### Example


```python
import gbs4api
from gbs4api.models.comment_dto import CommentDto
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
    api_instance = gbs4api.CommentControllerApi(api_client)
    external_test_id = 'external_test_id_example' # str | 
    pulse_test_customer_ref_number = 'pulse_test_customer_ref_number_example' # str | 
    test_facility_name = 'test_facility_name_example' # str | 
    pre_test_customer_ref_number = 'pre_test_customer_ref_number_example' # str | 
    body = 'body_example' # str | 

    try:
        api_response = api_instance.create_comment_for_pre_test(external_test_id, pulse_test_customer_ref_number, test_facility_name, pre_test_customer_ref_number, body)
        print("The response of CommentControllerApi->create_comment_for_pre_test:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling CommentControllerApi->create_comment_for_pre_test: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **external_test_id** | **str**|  | 
 **pulse_test_customer_ref_number** | **str**|  | 
 **test_facility_name** | **str**|  | 
 **pre_test_customer_ref_number** | **str**|  | 
 **body** | **str**|  | 

### Return type

[**CommentDto**](CommentDto.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: text/plain
 - **Accept**: */*

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**201** | Created |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **create_comment_for_pulse_test**
> CommentDto create_comment_for_pulse_test(external_test_id, pulse_test_customer_ref_number, body)

### Example


```python
import gbs4api
from gbs4api.models.comment_dto import CommentDto
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
    api_instance = gbs4api.CommentControllerApi(api_client)
    external_test_id = 'external_test_id_example' # str | 
    pulse_test_customer_ref_number = 'pulse_test_customer_ref_number_example' # str | 
    body = 'body_example' # str | 

    try:
        api_response = api_instance.create_comment_for_pulse_test(external_test_id, pulse_test_customer_ref_number, body)
        print("The response of CommentControllerApi->create_comment_for_pulse_test:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling CommentControllerApi->create_comment_for_pulse_test: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **external_test_id** | **str**|  | 
 **pulse_test_customer_ref_number** | **str**|  | 
 **body** | **str**|  | 

### Return type

[**CommentDto**](CommentDto.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: text/plain
 - **Accept**: */*

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**201** | Created |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_comments_for_external_test**
> List[CommentDto] get_comments_for_external_test(external_test_id)

### Example


```python
import gbs4api
from gbs4api.models.comment_dto import CommentDto
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
    api_instance = gbs4api.CommentControllerApi(api_client)
    external_test_id = 'external_test_id_example' # str | 

    try:
        api_response = api_instance.get_comments_for_external_test(external_test_id)
        print("The response of CommentControllerApi->get_comments_for_external_test:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling CommentControllerApi->get_comments_for_external_test: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **external_test_id** | **str**|  | 

### Return type

[**List[CommentDto]**](CommentDto.md)

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

# **get_comments_for_pre_test**
> List[CommentDto] get_comments_for_pre_test(external_test_id, pulse_test_customer_ref_number, test_facility_name, pre_test_customer_ref_number)

### Example


```python
import gbs4api
from gbs4api.models.comment_dto import CommentDto
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
    api_instance = gbs4api.CommentControllerApi(api_client)
    external_test_id = 'external_test_id_example' # str | 
    pulse_test_customer_ref_number = 'pulse_test_customer_ref_number_example' # str | 
    test_facility_name = 'test_facility_name_example' # str | 
    pre_test_customer_ref_number = 'pre_test_customer_ref_number_example' # str | 

    try:
        api_response = api_instance.get_comments_for_pre_test(external_test_id, pulse_test_customer_ref_number, test_facility_name, pre_test_customer_ref_number)
        print("The response of CommentControllerApi->get_comments_for_pre_test:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling CommentControllerApi->get_comments_for_pre_test: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **external_test_id** | **str**|  | 
 **pulse_test_customer_ref_number** | **str**|  | 
 **test_facility_name** | **str**|  | 
 **pre_test_customer_ref_number** | **str**|  | 

### Return type

[**List[CommentDto]**](CommentDto.md)

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

# **get_comments_for_pulse_test**
> List[CommentDto] get_comments_for_pulse_test(external_test_id, pulse_test_customer_ref_number)

### Example


```python
import gbs4api
from gbs4api.models.comment_dto import CommentDto
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
    api_instance = gbs4api.CommentControllerApi(api_client)
    external_test_id = 'external_test_id_example' # str | 
    pulse_test_customer_ref_number = 'pulse_test_customer_ref_number_example' # str | 

    try:
        api_response = api_instance.get_comments_for_pulse_test(external_test_id, pulse_test_customer_ref_number)
        print("The response of CommentControllerApi->get_comments_for_pulse_test:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling CommentControllerApi->get_comments_for_pulse_test: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **external_test_id** | **str**|  | 
 **pulse_test_customer_ref_number** | **str**|  | 

### Return type

[**List[CommentDto]**](CommentDto.md)

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

