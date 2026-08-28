# gbs3api.RequestApi

All URIs are relative to */GBS*

Method | HTTP request | Description
------------- | ------------- | -------------
[**exists_project**](RequestApi.md#exists_project) | **HEAD** /webservice/request/projects/{functionNumber} | Whether a project exists
[**exists_test**](RequestApi.md#exists_test) | **HEAD** /webservice/request/projects/{functionNumber}/series/{seriesNumber}/tests/{testNumber} | Whether a test exists
[**exists_test_series**](RequestApi.md#exists_test_series) | **HEAD** /webservice/request/projects/{functionNumber}/series/{seriesNumber} | Whether a series exists
[**find_project**](RequestApi.md#find_project) | **GET** /webservice/request/projects/{functionNumber} | Find a project
[**find_test**](RequestApi.md#find_test) | **GET** /webservice/request/projects/{functionNumber}/series/{seriesNumber}/tests/{testNumber} | Find a test
[**find_test_series**](RequestApi.md#find_test_series) | **GET** /webservice/request/projects/{functionNumber}/series/{seriesNumber} | Find a test series
[**find_test_series_details**](RequestApi.md#find_test_series_details) | **GET** /webservice/request/test-series-details | Find test series details
[**find_test_step_details**](RequestApi.md#find_test_step_details) | **GET** /webservice/request/test-step-details/{id} | Find test step schedule details
[**upload_data**](RequestApi.md#upload_data) | **PUT** /webservice/request/projects | Upload test data using TestDataXML format. This function is successor from &#39;testdata/project/upload&#39; , using enhanced authentication via GBSSecured.


# **exists_project**
> exists_project(function_number, include_definition=include_definition)

Whether a project exists

### Example

* Api Key Authentication (APIKeyV1):
* Api Key Authentication (CredentialsParameter):
* Basic Authentication (BasicAuth):
* Api Key Authentication (JWTCookie):
* Bearer (JWT) Authentication (JWT):

```python
import gbs3api
from gbs3api.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to /GBS
# See configuration.py for a list of all supported configuration parameters.
configuration = gbs3api.Configuration(
    host = "/GBS"
)

# The client must configure the authentication and authorization parameters
# in accordance with the API server security policy.
# Examples for each auth method are provided below, use the example that
# satisfies your auth use case.

# Configure API key authorization: APIKeyV1
configuration.api_key['APIKeyV1'] = os.environ["API_KEY"]

# Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
# configuration.api_key_prefix['APIKeyV1'] = 'Bearer'

# Configure API key authorization: CredentialsParameter
configuration.api_key['CredentialsParameter'] = os.environ["API_KEY"]

# Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
# configuration.api_key_prefix['CredentialsParameter'] = 'Bearer'

# Configure HTTP basic authorization: BasicAuth
configuration = gbs3api.Configuration(
    username = os.environ["USERNAME"],
    password = os.environ["PASSWORD"]
)

# Configure API key authorization: JWTCookie
configuration.api_key['JWTCookie'] = os.environ["API_KEY"]

# Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
# configuration.api_key_prefix['JWTCookie'] = 'Bearer'

# Configure Bearer authorization (JWT): JWT
configuration = gbs3api.Configuration(
    access_token = os.environ["BEARER_TOKEN"]
)

# Enter a context with an instance of the API client
with gbs3api.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = gbs3api.RequestApi(api_client)
    function_number = 'function_number_example' # str | 
    include_definition = True # bool |  (optional) (default to True)

    try:
        # Whether a project exists
        api_instance.exists_project(function_number, include_definition=include_definition)
    except Exception as e:
        print("Exception when calling RequestApi->exists_project: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **function_number** | **str**|  | 
 **include_definition** | **bool**|  | [optional] [default to True]

### Return type

void (empty response body)

### Authorization

[APIKeyV1](../README.md#APIKeyV1), [CredentialsParameter](../README.md#CredentialsParameter), [BasicAuth](../README.md#BasicAuth), [JWTCookie](../README.md#JWTCookie), [JWT](../README.md#JWT)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: Not defined

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Project found |  -  |
**404** | Project not found |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **exists_test**
> exists_test(function_number, series_number, test_number, include_definition=include_definition)

Whether a test exists

### Example

* Api Key Authentication (APIKeyV1):
* Api Key Authentication (CredentialsParameter):
* Basic Authentication (BasicAuth):
* Api Key Authentication (JWTCookie):
* Bearer (JWT) Authentication (JWT):

```python
import gbs3api
from gbs3api.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to /GBS
# See configuration.py for a list of all supported configuration parameters.
configuration = gbs3api.Configuration(
    host = "/GBS"
)

# The client must configure the authentication and authorization parameters
# in accordance with the API server security policy.
# Examples for each auth method are provided below, use the example that
# satisfies your auth use case.

# Configure API key authorization: APIKeyV1
configuration.api_key['APIKeyV1'] = os.environ["API_KEY"]

# Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
# configuration.api_key_prefix['APIKeyV1'] = 'Bearer'

# Configure API key authorization: CredentialsParameter
configuration.api_key['CredentialsParameter'] = os.environ["API_KEY"]

# Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
# configuration.api_key_prefix['CredentialsParameter'] = 'Bearer'

# Configure HTTP basic authorization: BasicAuth
configuration = gbs3api.Configuration(
    username = os.environ["USERNAME"],
    password = os.environ["PASSWORD"]
)

# Configure API key authorization: JWTCookie
configuration.api_key['JWTCookie'] = os.environ["API_KEY"]

# Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
# configuration.api_key_prefix['JWTCookie'] = 'Bearer'

# Configure Bearer authorization (JWT): JWT
configuration = gbs3api.Configuration(
    access_token = os.environ["BEARER_TOKEN"]
)

# Enter a context with an instance of the API client
with gbs3api.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = gbs3api.RequestApi(api_client)
    function_number = 'function_number_example' # str | 
    series_number = 'series_number_example' # str | 
    test_number = 'test_number_example' # str | 
    include_definition = True # bool |  (optional) (default to True)

    try:
        # Whether a test exists
        api_instance.exists_test(function_number, series_number, test_number, include_definition=include_definition)
    except Exception as e:
        print("Exception when calling RequestApi->exists_test: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **function_number** | **str**|  | 
 **series_number** | **str**|  | 
 **test_number** | **str**|  | 
 **include_definition** | **bool**|  | [optional] [default to True]

### Return type

void (empty response body)

### Authorization

[APIKeyV1](../README.md#APIKeyV1), [CredentialsParameter](../README.md#CredentialsParameter), [BasicAuth](../README.md#BasicAuth), [JWTCookie](../README.md#JWTCookie), [JWT](../README.md#JWT)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: Not defined

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Test found |  -  |
**404** | Test not found |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **exists_test_series**
> exists_test_series(function_number, series_number, include_definition=include_definition)

Whether a series exists

### Example

* Api Key Authentication (APIKeyV1):
* Api Key Authentication (CredentialsParameter):
* Basic Authentication (BasicAuth):
* Api Key Authentication (JWTCookie):
* Bearer (JWT) Authentication (JWT):

```python
import gbs3api
from gbs3api.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to /GBS
# See configuration.py for a list of all supported configuration parameters.
configuration = gbs3api.Configuration(
    host = "/GBS"
)

# The client must configure the authentication and authorization parameters
# in accordance with the API server security policy.
# Examples for each auth method are provided below, use the example that
# satisfies your auth use case.

# Configure API key authorization: APIKeyV1
configuration.api_key['APIKeyV1'] = os.environ["API_KEY"]

# Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
# configuration.api_key_prefix['APIKeyV1'] = 'Bearer'

# Configure API key authorization: CredentialsParameter
configuration.api_key['CredentialsParameter'] = os.environ["API_KEY"]

# Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
# configuration.api_key_prefix['CredentialsParameter'] = 'Bearer'

# Configure HTTP basic authorization: BasicAuth
configuration = gbs3api.Configuration(
    username = os.environ["USERNAME"],
    password = os.environ["PASSWORD"]
)

# Configure API key authorization: JWTCookie
configuration.api_key['JWTCookie'] = os.environ["API_KEY"]

# Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
# configuration.api_key_prefix['JWTCookie'] = 'Bearer'

# Configure Bearer authorization (JWT): JWT
configuration = gbs3api.Configuration(
    access_token = os.environ["BEARER_TOKEN"]
)

# Enter a context with an instance of the API client
with gbs3api.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = gbs3api.RequestApi(api_client)
    function_number = 'function_number_example' # str | 
    series_number = 'series_number_example' # str | 
    include_definition = True # bool |  (optional) (default to True)

    try:
        # Whether a series exists
        api_instance.exists_test_series(function_number, series_number, include_definition=include_definition)
    except Exception as e:
        print("Exception when calling RequestApi->exists_test_series: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **function_number** | **str**|  | 
 **series_number** | **str**|  | 
 **include_definition** | **bool**|  | [optional] [default to True]

### Return type

void (empty response body)

### Authorization

[APIKeyV1](../README.md#APIKeyV1), [CredentialsParameter](../README.md#CredentialsParameter), [BasicAuth](../README.md#BasicAuth), [JWTCookie](../README.md#JWTCookie), [JWT](../README.md#JWT)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: Not defined

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Series found |  -  |
**404** | Series not found |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **find_project**
> ProjectDataType find_project(function_number, include_definition=include_definition)

Find a project

### Example

* Api Key Authentication (APIKeyV1):
* Api Key Authentication (CredentialsParameter):
* Basic Authentication (BasicAuth):
* Api Key Authentication (JWTCookie):
* Bearer (JWT) Authentication (JWT):

```python
import gbs3api
from gbs3api.models.project_data_type import ProjectDataType
from gbs3api.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to /GBS
# See configuration.py for a list of all supported configuration parameters.
configuration = gbs3api.Configuration(
    host = "/GBS"
)

# The client must configure the authentication and authorization parameters
# in accordance with the API server security policy.
# Examples for each auth method are provided below, use the example that
# satisfies your auth use case.

# Configure API key authorization: APIKeyV1
configuration.api_key['APIKeyV1'] = os.environ["API_KEY"]

# Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
# configuration.api_key_prefix['APIKeyV1'] = 'Bearer'

# Configure API key authorization: CredentialsParameter
configuration.api_key['CredentialsParameter'] = os.environ["API_KEY"]

# Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
# configuration.api_key_prefix['CredentialsParameter'] = 'Bearer'

# Configure HTTP basic authorization: BasicAuth
configuration = gbs3api.Configuration(
    username = os.environ["USERNAME"],
    password = os.environ["PASSWORD"]
)

# Configure API key authorization: JWTCookie
configuration.api_key['JWTCookie'] = os.environ["API_KEY"]

# Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
# configuration.api_key_prefix['JWTCookie'] = 'Bearer'

# Configure Bearer authorization (JWT): JWT
configuration = gbs3api.Configuration(
    access_token = os.environ["BEARER_TOKEN"]
)

# Enter a context with an instance of the API client
with gbs3api.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = gbs3api.RequestApi(api_client)
    function_number = 'function_number_example' # str | 
    include_definition = True # bool |  (optional) (default to True)

    try:
        # Find a project
        api_response = api_instance.find_project(function_number, include_definition=include_definition)
        print("The response of RequestApi->find_project:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling RequestApi->find_project: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **function_number** | **str**|  | 
 **include_definition** | **bool**|  | [optional] [default to True]

### Return type

[**ProjectDataType**](ProjectDataType.md)

### Authorization

[APIKeyV1](../README.md#APIKeyV1), [CredentialsParameter](../README.md#CredentialsParameter), [BasicAuth](../README.md#BasicAuth), [JWTCookie](../README.md#JWTCookie), [JWT](../README.md#JWT)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Project found |  -  |
**404** | Project not found |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **find_test**
> TestDataType find_test(function_number, series_number, test_number, include_definition=include_definition)

Find a test

### Example

* Api Key Authentication (APIKeyV1):
* Api Key Authentication (CredentialsParameter):
* Basic Authentication (BasicAuth):
* Api Key Authentication (JWTCookie):
* Bearer (JWT) Authentication (JWT):

```python
import gbs3api
from gbs3api.models.test_data_type import TestDataType
from gbs3api.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to /GBS
# See configuration.py for a list of all supported configuration parameters.
configuration = gbs3api.Configuration(
    host = "/GBS"
)

# The client must configure the authentication and authorization parameters
# in accordance with the API server security policy.
# Examples for each auth method are provided below, use the example that
# satisfies your auth use case.

# Configure API key authorization: APIKeyV1
configuration.api_key['APIKeyV1'] = os.environ["API_KEY"]

# Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
# configuration.api_key_prefix['APIKeyV1'] = 'Bearer'

# Configure API key authorization: CredentialsParameter
configuration.api_key['CredentialsParameter'] = os.environ["API_KEY"]

# Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
# configuration.api_key_prefix['CredentialsParameter'] = 'Bearer'

# Configure HTTP basic authorization: BasicAuth
configuration = gbs3api.Configuration(
    username = os.environ["USERNAME"],
    password = os.environ["PASSWORD"]
)

# Configure API key authorization: JWTCookie
configuration.api_key['JWTCookie'] = os.environ["API_KEY"]

# Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
# configuration.api_key_prefix['JWTCookie'] = 'Bearer'

# Configure Bearer authorization (JWT): JWT
configuration = gbs3api.Configuration(
    access_token = os.environ["BEARER_TOKEN"]
)

# Enter a context with an instance of the API client
with gbs3api.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = gbs3api.RequestApi(api_client)
    function_number = 'function_number_example' # str | 
    series_number = 'series_number_example' # str | 
    test_number = 'test_number_example' # str | 
    include_definition = True # bool |  (optional) (default to True)

    try:
        # Find a test
        api_response = api_instance.find_test(function_number, series_number, test_number, include_definition=include_definition)
        print("The response of RequestApi->find_test:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling RequestApi->find_test: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **function_number** | **str**|  | 
 **series_number** | **str**|  | 
 **test_number** | **str**|  | 
 **include_definition** | **bool**|  | [optional] [default to True]

### Return type

[**TestDataType**](TestDataType.md)

### Authorization

[APIKeyV1](../README.md#APIKeyV1), [CredentialsParameter](../README.md#CredentialsParameter), [BasicAuth](../README.md#BasicAuth), [JWTCookie](../README.md#JWTCookie), [JWT](../README.md#JWT)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Test found |  -  |
**404** | Test not found |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **find_test_series**
> TestSeriesDataType find_test_series(function_number, series_number, include_definition=include_definition)

Find a test series

Optional fields are omitted from the JSON response instead of being serialized as null. To satisfy required schema fields, missing dateOfTheTest values are filled with the current timestamp during response mapping.

### Example

* Api Key Authentication (APIKeyV1):
* Api Key Authentication (CredentialsParameter):
* Basic Authentication (BasicAuth):
* Api Key Authentication (JWTCookie):
* Bearer (JWT) Authentication (JWT):

```python
import gbs3api
from gbs3api.models.test_series_data_type import TestSeriesDataType
from gbs3api.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to /GBS
# See configuration.py for a list of all supported configuration parameters.
configuration = gbs3api.Configuration(
    host = "/GBS"
)

# The client must configure the authentication and authorization parameters
# in accordance with the API server security policy.
# Examples for each auth method are provided below, use the example that
# satisfies your auth use case.

# Configure API key authorization: APIKeyV1
configuration.api_key['APIKeyV1'] = os.environ["API_KEY"]

# Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
# configuration.api_key_prefix['APIKeyV1'] = 'Bearer'

# Configure API key authorization: CredentialsParameter
configuration.api_key['CredentialsParameter'] = os.environ["API_KEY"]

# Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
# configuration.api_key_prefix['CredentialsParameter'] = 'Bearer'

# Configure HTTP basic authorization: BasicAuth
configuration = gbs3api.Configuration(
    username = os.environ["USERNAME"],
    password = os.environ["PASSWORD"]
)

# Configure API key authorization: JWTCookie
configuration.api_key['JWTCookie'] = os.environ["API_KEY"]

# Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
# configuration.api_key_prefix['JWTCookie'] = 'Bearer'

# Configure Bearer authorization (JWT): JWT
configuration = gbs3api.Configuration(
    access_token = os.environ["BEARER_TOKEN"]
)

# Enter a context with an instance of the API client
with gbs3api.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = gbs3api.RequestApi(api_client)
    function_number = 'function_number_example' # str | 
    series_number = 'series_number_example' # str | 
    include_definition = True # bool |  (optional) (default to True)

    try:
        # Find a test series
        api_response = api_instance.find_test_series(function_number, series_number, include_definition=include_definition)
        print("The response of RequestApi->find_test_series:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling RequestApi->find_test_series: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **function_number** | **str**|  | 
 **series_number** | **str**|  | 
 **include_definition** | **bool**|  | [optional] [default to True]

### Return type

[**TestSeriesDataType**](TestSeriesDataType.md)

### Authorization

[APIKeyV1](../README.md#APIKeyV1), [CredentialsParameter](../README.md#CredentialsParameter), [BasicAuth](../README.md#BasicAuth), [JWTCookie](../README.md#JWTCookie), [JWT](../README.md#JWT)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Series found |  -  |
**404** | Series not found |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **find_test_series_details**
> TestSeriesDetailsDTO find_test_series_details(full_series_number=full_series_number)

Find test series details

### Example

* Api Key Authentication (APIKeyV1):
* Api Key Authentication (CredentialsParameter):
* Basic Authentication (BasicAuth):
* Api Key Authentication (JWTCookie):
* Bearer (JWT) Authentication (JWT):

```python
import gbs3api
from gbs3api.models.test_series_details_dto import TestSeriesDetailsDTO
from gbs3api.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to /GBS
# See configuration.py for a list of all supported configuration parameters.
configuration = gbs3api.Configuration(
    host = "/GBS"
)

# The client must configure the authentication and authorization parameters
# in accordance with the API server security policy.
# Examples for each auth method are provided below, use the example that
# satisfies your auth use case.

# Configure API key authorization: APIKeyV1
configuration.api_key['APIKeyV1'] = os.environ["API_KEY"]

# Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
# configuration.api_key_prefix['APIKeyV1'] = 'Bearer'

# Configure API key authorization: CredentialsParameter
configuration.api_key['CredentialsParameter'] = os.environ["API_KEY"]

# Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
# configuration.api_key_prefix['CredentialsParameter'] = 'Bearer'

# Configure HTTP basic authorization: BasicAuth
configuration = gbs3api.Configuration(
    username = os.environ["USERNAME"],
    password = os.environ["PASSWORD"]
)

# Configure API key authorization: JWTCookie
configuration.api_key['JWTCookie'] = os.environ["API_KEY"]

# Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
# configuration.api_key_prefix['JWTCookie'] = 'Bearer'

# Configure Bearer authorization (JWT): JWT
configuration = gbs3api.Configuration(
    access_token = os.environ["BEARER_TOKEN"]
)

# Enter a context with an instance of the API client
with gbs3api.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = gbs3api.RequestApi(api_client)
    full_series_number = 'full_series_number_example' # str |  (optional)

    try:
        # Find test series details
        api_response = api_instance.find_test_series_details(full_series_number=full_series_number)
        print("The response of RequestApi->find_test_series_details:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling RequestApi->find_test_series_details: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **full_series_number** | **str**|  | [optional] 

### Return type

[**TestSeriesDetailsDTO**](TestSeriesDetailsDTO.md)

### Authorization

[APIKeyV1](../README.md#APIKeyV1), [CredentialsParameter](../README.md#CredentialsParameter), [BasicAuth](../README.md#BasicAuth), [JWTCookie](../README.md#JWTCookie), [JWT](../README.md#JWT)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Test series details found |  -  |
**400** | Full series number is missing |  -  |
**404** | Test series details not found |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **find_test_step_details**
> TestStepDetailsDTO find_test_step_details(id)

Find test step schedule details

### Example

* Api Key Authentication (APIKeyV1):
* Api Key Authentication (CredentialsParameter):
* Basic Authentication (BasicAuth):
* Api Key Authentication (JWTCookie):
* Bearer (JWT) Authentication (JWT):

```python
import gbs3api
from gbs3api.models.test_step_details_dto import TestStepDetailsDTO
from gbs3api.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to /GBS
# See configuration.py for a list of all supported configuration parameters.
configuration = gbs3api.Configuration(
    host = "/GBS"
)

# The client must configure the authentication and authorization parameters
# in accordance with the API server security policy.
# Examples for each auth method are provided below, use the example that
# satisfies your auth use case.

# Configure API key authorization: APIKeyV1
configuration.api_key['APIKeyV1'] = os.environ["API_KEY"]

# Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
# configuration.api_key_prefix['APIKeyV1'] = 'Bearer'

# Configure API key authorization: CredentialsParameter
configuration.api_key['CredentialsParameter'] = os.environ["API_KEY"]

# Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
# configuration.api_key_prefix['CredentialsParameter'] = 'Bearer'

# Configure HTTP basic authorization: BasicAuth
configuration = gbs3api.Configuration(
    username = os.environ["USERNAME"],
    password = os.environ["PASSWORD"]
)

# Configure API key authorization: JWTCookie
configuration.api_key['JWTCookie'] = os.environ["API_KEY"]

# Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
# configuration.api_key_prefix['JWTCookie'] = 'Bearer'

# Configure Bearer authorization (JWT): JWT
configuration = gbs3api.Configuration(
    access_token = os.environ["BEARER_TOKEN"]
)

# Enter a context with an instance of the API client
with gbs3api.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = gbs3api.RequestApi(api_client)
    id = 56 # int | 

    try:
        # Find test step schedule details
        api_response = api_instance.find_test_step_details(id)
        print("The response of RequestApi->find_test_step_details:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling RequestApi->find_test_step_details: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **int**|  | 

### Return type

[**TestStepDetailsDTO**](TestStepDetailsDTO.md)

### Authorization

[APIKeyV1](../README.md#APIKeyV1), [CredentialsParameter](../README.md#CredentialsParameter), [BasicAuth](../README.md#BasicAuth), [JWTCookie](../README.md#JWTCookie), [JWT](../README.md#JWT)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Test step details found |  -  |
**404** | Test step details not found |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **upload_data**
> upload_data(body=body)

Upload test data using TestDataXML format. This function is successor from 'testdata/project/upload' , using enhanced authentication via GBSSecured.

### Example

* Api Key Authentication (APIKeyV1):
* Api Key Authentication (CredentialsParameter):
* Basic Authentication (BasicAuth):
* Api Key Authentication (JWTCookie):
* Bearer (JWT) Authentication (JWT):

```python
import gbs3api
from gbs3api.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to /GBS
# See configuration.py for a list of all supported configuration parameters.
configuration = gbs3api.Configuration(
    host = "/GBS"
)

# The client must configure the authentication and authorization parameters
# in accordance with the API server security policy.
# Examples for each auth method are provided below, use the example that
# satisfies your auth use case.

# Configure API key authorization: APIKeyV1
configuration.api_key['APIKeyV1'] = os.environ["API_KEY"]

# Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
# configuration.api_key_prefix['APIKeyV1'] = 'Bearer'

# Configure API key authorization: CredentialsParameter
configuration.api_key['CredentialsParameter'] = os.environ["API_KEY"]

# Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
# configuration.api_key_prefix['CredentialsParameter'] = 'Bearer'

# Configure HTTP basic authorization: BasicAuth
configuration = gbs3api.Configuration(
    username = os.environ["USERNAME"],
    password = os.environ["PASSWORD"]
)

# Configure API key authorization: JWTCookie
configuration.api_key['JWTCookie'] = os.environ["API_KEY"]

# Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
# configuration.api_key_prefix['JWTCookie'] = 'Bearer'

# Configure Bearer authorization (JWT): JWT
configuration = gbs3api.Configuration(
    access_token = os.environ["BEARER_TOKEN"]
)

# Enter a context with an instance of the API client
with gbs3api.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = gbs3api.RequestApi(api_client)
    body = None # bytearray |  (optional)

    try:
        # Upload test data using TestDataXML format. This function is successor from 'testdata/project/upload' , using enhanced authentication via GBSSecured.
        api_instance.upload_data(body=body)
    except Exception as e:
        print("Exception when calling RequestApi->upload_data: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | **bytearray**|  | [optional] 

### Return type

void (empty response body)

### Authorization

[APIKeyV1](../README.md#APIKeyV1), [CredentialsParameter](../README.md#CredentialsParameter), [BasicAuth](../README.md#BasicAuth), [JWTCookie](../README.md#JWTCookie), [JWT](../README.md#JWT)

### HTTP request headers

 - **Content-Type**: application/xml
 - **Accept**: text/plain

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Upload successful |  -  |
**404** | No Test found in GBS for given testnumber |  -  |
**500** | Internal server error, contact GBS Support |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

