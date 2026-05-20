# gbs4api.ExternalTestControllerApi

All URIs are relative to *https://alfpwin0044.corp.passivesafety.com/gbs4-api*

Method | HTTP request | Description
------------- | ------------- | -------------
[**create_external_test**](ExternalTestControllerApi.md#create_external_test) | **POST** /api/v1/external-tests | 
[**create_external_test_from_mme**](ExternalTestControllerApi.md#create_external_test_from_mme) | **POST** /api/v1/external-tests/mme | 
[**delete_external_test**](ExternalTestControllerApi.md#delete_external_test) | **DELETE** /api/v1/external-tests/{externalTestId} | 
[**get_external_test_by_test_id**](ExternalTestControllerApi.md#get_external_test_by_test_id) | **GET** /api/v1/external-tests/{externalTestId} | 
[**get_external_tests**](ExternalTestControllerApi.md#get_external_tests) | **GET** /api/v1/external-tests | 
[**update_external_test**](ExternalTestControllerApi.md#update_external_test) | **PUT** /api/v1/external-tests/{externalTestId} | 
[**update_external_test_from_mme**](ExternalTestControllerApi.md#update_external_test_from_mme) | **PUT** /api/v1/external-tests/mme/{externalTestId} | 
[**upload_report_for_external_test**](ExternalTestControllerApi.md#upload_report_for_external_test) | **PUT** /api/v1/external-tests/{externalTestId}/pdf | 


# **create_external_test**
> create_external_test(external_test_dto)

### Example


```python
import gbs4api
from gbs4api.models.external_test_dto import ExternalTestDto
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
    api_instance = gbs4api.ExternalTestControllerApi(api_client)
    external_test_dto = gbs4api.ExternalTestDto() # ExternalTestDto | 

    try:
        api_instance.create_external_test(external_test_dto)
    except Exception as e:
        print("Exception when calling ExternalTestControllerApi->create_external_test: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **external_test_dto** | [**ExternalTestDto**](ExternalTestDto.md)|  | 

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

# **create_external_test_from_mme**
> ExternalTestDto create_external_test_from_mme(files=files)

### Example


```python
import gbs4api
from gbs4api.models.external_test_dto import ExternalTestDto
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
    api_instance = gbs4api.ExternalTestControllerApi(api_client)
    files = None # List[bytes] |  (optional)

    try:
        api_response = api_instance.create_external_test_from_mme(files=files)
        print("The response of ExternalTestControllerApi->create_external_test_from_mme:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling ExternalTestControllerApi->create_external_test_from_mme: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **files** | **List[bytes]**|  | [optional] 

### Return type

[**ExternalTestDto**](ExternalTestDto.md)

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

# **delete_external_test**
> delete_external_test(external_test_id)

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
    api_instance = gbs4api.ExternalTestControllerApi(api_client)
    external_test_id = 'external_test_id_example' # str | 

    try:
        api_instance.delete_external_test(external_test_id)
    except Exception as e:
        print("Exception when calling ExternalTestControllerApi->delete_external_test: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **external_test_id** | **str**|  | 

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

# **get_external_test_by_test_id**
> ExternalTestDto get_external_test_by_test_id(external_test_id)

### Example


```python
import gbs4api
from gbs4api.models.external_test_dto import ExternalTestDto
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
    api_instance = gbs4api.ExternalTestControllerApi(api_client)
    external_test_id = 'external_test_id_example' # str | 

    try:
        api_response = api_instance.get_external_test_by_test_id(external_test_id)
        print("The response of ExternalTestControllerApi->get_external_test_by_test_id:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling ExternalTestControllerApi->get_external_test_by_test_id: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **external_test_id** | **str**|  | 

### Return type

[**ExternalTestDto**](ExternalTestDto.md)

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

# **get_external_tests**
> List[ExternalTestDto] get_external_tests(filter=filter, items_per_page=items_per_page, page=page)

### Example


```python
import gbs4api
from gbs4api.models.external_test_dto import ExternalTestDto
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
    api_instance = gbs4api.ExternalTestControllerApi(api_client)
    filter = 'filter_example' # str |  (optional)
    items_per_page = 56 # int |  (optional)
    page = 56 # int |  (optional)

    try:
        api_response = api_instance.get_external_tests(filter=filter, items_per_page=items_per_page, page=page)
        print("The response of ExternalTestControllerApi->get_external_tests:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling ExternalTestControllerApi->get_external_tests: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **filter** | **str**|  | [optional] 
 **items_per_page** | **int**|  | [optional] 
 **page** | **int**|  | [optional] 

### Return type

[**List[ExternalTestDto]**](ExternalTestDto.md)

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

# **update_external_test**
> update_external_test(external_test_id, external_test_dto)

### Example


```python
import gbs4api
from gbs4api.models.external_test_dto import ExternalTestDto
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
    api_instance = gbs4api.ExternalTestControllerApi(api_client)
    external_test_id = 'external_test_id_example' # str | 
    external_test_dto = gbs4api.ExternalTestDto() # ExternalTestDto | 

    try:
        api_instance.update_external_test(external_test_id, external_test_dto)
    except Exception as e:
        print("Exception when calling ExternalTestControllerApi->update_external_test: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **external_test_id** | **str**|  | 
 **external_test_dto** | [**ExternalTestDto**](ExternalTestDto.md)|  | 

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

# **update_external_test_from_mme**
> ExternalTestDto update_external_test_from_mme(external_test_id, force, files=files)

### Example


```python
import gbs4api
from gbs4api.models.external_test_dto import ExternalTestDto
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
    api_instance = gbs4api.ExternalTestControllerApi(api_client)
    external_test_id = 'external_test_id_example' # str | 
    force = True # bool | 
    files = None # List[bytes] |  (optional)

    try:
        api_response = api_instance.update_external_test_from_mme(external_test_id, force, files=files)
        print("The response of ExternalTestControllerApi->update_external_test_from_mme:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling ExternalTestControllerApi->update_external_test_from_mme: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **external_test_id** | **str**|  | 
 **force** | **bool**|  | 
 **files** | **List[bytes]**|  | [optional] 

### Return type

[**ExternalTestDto**](ExternalTestDto.md)

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

# **upload_report_for_external_test**
> str upload_report_for_external_test(external_test_id, file)

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
    api_instance = gbs4api.ExternalTestControllerApi(api_client)
    external_test_id = 'external_test_id_example' # str | 
    file = None # bytes | 

    try:
        api_response = api_instance.upload_report_for_external_test(external_test_id, file)
        print("The response of ExternalTestControllerApi->upload_report_for_external_test:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling ExternalTestControllerApi->upload_report_for_external_test: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **external_test_id** | **str**|  | 
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

