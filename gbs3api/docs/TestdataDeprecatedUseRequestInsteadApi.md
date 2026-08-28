# gbs3api.TestdataDeprecatedUseRequestInsteadApi

All URIs are relative to */GBS*

Method | HTTP request | Description
------------- | ------------- | -------------
[**export_project**](TestdataDeprecatedUseRequestInsteadApi.md#export_project) | **GET** /webservice/testdata/project/export | 
[**export_test**](TestdataDeprecatedUseRequestInsteadApi.md#export_test) | **GET** /webservice/testdata/test/export | 
[**export_test_series**](TestdataDeprecatedUseRequestInsteadApi.md#export_test_series) | **GET** /webservice/testdata/testSeries/export | 
[**list_of_project**](TestdataDeprecatedUseRequestInsteadApi.md#list_of_project) | **GET** /webservice/testdata/project/list | 
[**project_exist**](TestdataDeprecatedUseRequestInsteadApi.md#project_exist) | **GET** /webservice/testdata/project/exist | 
[**test_exist**](TestdataDeprecatedUseRequestInsteadApi.md#test_exist) | **GET** /webservice/testdata/test/exist | 
[**test_series_exist**](TestdataDeprecatedUseRequestInsteadApi.md#test_series_exist) | **GET** /webservice/testdata/testSeries/exist | 
[**upload_data1**](TestdataDeprecatedUseRequestInsteadApi.md#upload_data1) | **POST** /webservice/testdata/project/upload | DEPRECATED! Use PUT instead of POST; Upload test data using TestDataXML format.
[**upload_test_data**](TestdataDeprecatedUseRequestInsteadApi.md#upload_test_data) | **PUT** /webservice/testdata/project/upload | Upload test data using TestDataXML format.


# **export_project**
> export_project(function_number=function_number, include_definition=include_definition)

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
    api_instance = gbs3api.TestdataDeprecatedUseRequestInsteadApi(api_client)
    function_number = 'function_number_example' # str |  (optional)
    include_definition = True # bool |  (optional) (default to True)

    try:
        api_instance.export_project(function_number=function_number, include_definition=include_definition)
    except Exception as e:
        print("Exception when calling TestdataDeprecatedUseRequestInsteadApi->export_project: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **function_number** | **str**|  | [optional] 
 **include_definition** | **bool**|  | [optional] [default to True]

### Return type

void (empty response body)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/xml

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**0** | default response |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **export_test**
> export_test(test_number=test_number, include_definition=include_definition, include_project=include_project)

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
    api_instance = gbs3api.TestdataDeprecatedUseRequestInsteadApi(api_client)
    test_number = 'test_number_example' # str |  (optional)
    include_definition = True # bool |  (optional) (default to True)
    include_project = True # bool |  (optional) (default to True)

    try:
        api_instance.export_test(test_number=test_number, include_definition=include_definition, include_project=include_project)
    except Exception as e:
        print("Exception when calling TestdataDeprecatedUseRequestInsteadApi->export_test: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **test_number** | **str**|  | [optional] 
 **include_definition** | **bool**|  | [optional] [default to True]
 **include_project** | **bool**|  | [optional] [default to True]

### Return type

void (empty response body)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/xml

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**0** | default response |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **export_test_series**
> export_test_series(function_number=function_number, test_series_number=test_series_number, include_definition=include_definition)

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
    api_instance = gbs3api.TestdataDeprecatedUseRequestInsteadApi(api_client)
    function_number = 'function_number_example' # str |  (optional)
    test_series_number = 'test_series_number_example' # str |  (optional)
    include_definition = True # bool |  (optional) (default to True)

    try:
        api_instance.export_test_series(function_number=function_number, test_series_number=test_series_number, include_definition=include_definition)
    except Exception as e:
        print("Exception when calling TestdataDeprecatedUseRequestInsteadApi->export_test_series: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **function_number** | **str**|  | [optional] 
 **test_series_number** | **str**|  | [optional] 
 **include_definition** | **bool**|  | [optional] [default to True]

### Return type

void (empty response body)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/xml

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**0** | default response |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **list_of_project**
> list_of_project(function_number=function_number, include_definition=include_definition)

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
    api_instance = gbs3api.TestdataDeprecatedUseRequestInsteadApi(api_client)
    function_number = 'function_number_example' # str |  (optional)
    include_definition = True # bool |  (optional) (default to True)

    try:
        api_instance.list_of_project(function_number=function_number, include_definition=include_definition)
    except Exception as e:
        print("Exception when calling TestdataDeprecatedUseRequestInsteadApi->list_of_project: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **function_number** | **str**|  | [optional] 
 **include_definition** | **bool**|  | [optional] [default to True]

### Return type

void (empty response body)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/xml

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**0** | default response |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **project_exist**
> project_exist(function_number=function_number)

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
    api_instance = gbs3api.TestdataDeprecatedUseRequestInsteadApi(api_client)
    function_number = 'function_number_example' # str |  (optional)

    try:
        api_instance.project_exist(function_number=function_number)
    except Exception as e:
        print("Exception when calling TestdataDeprecatedUseRequestInsteadApi->project_exist: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **function_number** | **str**|  | [optional] 

### Return type

void (empty response body)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: text/plain

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**0** | default response |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **test_exist**
> test_exist(test_number=test_number)

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
    api_instance = gbs3api.TestdataDeprecatedUseRequestInsteadApi(api_client)
    test_number = 'test_number_example' # str |  (optional)

    try:
        api_instance.test_exist(test_number=test_number)
    except Exception as e:
        print("Exception when calling TestdataDeprecatedUseRequestInsteadApi->test_exist: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **test_number** | **str**|  | [optional] 

### Return type

void (empty response body)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: text/plain

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**0** | default response |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **test_series_exist**
> test_series_exist(function_number=function_number, test_series_number=test_series_number)

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
    api_instance = gbs3api.TestdataDeprecatedUseRequestInsteadApi(api_client)
    function_number = 'function_number_example' # str |  (optional)
    test_series_number = 'test_series_number_example' # str |  (optional)

    try:
        api_instance.test_series_exist(function_number=function_number, test_series_number=test_series_number)
    except Exception as e:
        print("Exception when calling TestdataDeprecatedUseRequestInsteadApi->test_series_exist: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **function_number** | **str**|  | [optional] 
 **test_series_number** | **str**|  | [optional] 

### Return type

void (empty response body)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: text/plain

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**0** | default response |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **upload_data1**
> upload_data1(body=body)

DEPRECATED! Use PUT instead of POST; Upload test data using TestDataXML format.

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
    api_instance = gbs3api.TestdataDeprecatedUseRequestInsteadApi(api_client)
    body = None # bytearray |  (optional)

    try:
        # DEPRECATED! Use PUT instead of POST; Upload test data using TestDataXML format.
        api_instance.upload_data1(body=body)
    except Exception as e:
        print("Exception when calling TestdataDeprecatedUseRequestInsteadApi->upload_data1: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | **bytearray**|  | [optional] 

### Return type

void (empty response body)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/xml
 - **Accept**: text/plain

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**0** | default response |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **upload_test_data**
> upload_test_data(body=body)

Upload test data using TestDataXML format.

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
    api_instance = gbs3api.TestdataDeprecatedUseRequestInsteadApi(api_client)
    body = None # bytearray |  (optional)

    try:
        # Upload test data using TestDataXML format.
        api_instance.upload_test_data(body=body)
    except Exception as e:
        print("Exception when calling TestdataDeprecatedUseRequestInsteadApi->upload_test_data: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | **bytearray**|  | [optional] 

### Return type

void (empty response body)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/xml
 - **Accept**: text/plain

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**0** | default response |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

