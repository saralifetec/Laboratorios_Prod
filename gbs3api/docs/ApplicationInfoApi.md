# gbs3api.ApplicationInfoApi

All URIs are relative to */GBS*

Method | HTTP request | Description
------------- | ------------- | -------------
[**delete_message**](ApplicationInfoApi.md#delete_message) | **DELETE** /webservice/applications/messages | Delete a message
[**get_languages**](ApplicationInfoApi.md#get_languages) | **GET** /webservice/applications/messages/languages | Get a list of all available languages
[**get_messages**](ApplicationInfoApi.md#get_messages) | **GET** /webservice/applications/messages | Get the messages for the specified application and languages; Gets language from header if none specified
[**get_modules**](ApplicationInfoApi.md#get_modules) | **GET** /webservice/applications/messages/modules | Get a list of all available modules
[**save_messages**](ApplicationInfoApi.md#save_messages) | **PUT** /webservice/applications/messages | Create or update messages


# **delete_message**
> delete_message(module=module, language=language, key=key)

Delete a message

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
    api_instance = gbs3api.ApplicationInfoApi(api_client)
    module = 'module_example' # str |  (optional)
    language = 'language_example' # str |  (optional)
    key = 'key_example' # str |  (optional)

    try:
        # Delete a message
        api_instance.delete_message(module=module, language=language, key=key)
    except Exception as e:
        print("Exception when calling ApplicationInfoApi->delete_message: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **module** | **str**|  | [optional] 
 **language** | **str**|  | [optional] 
 **key** | **str**|  | [optional] 

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
**204** | Deleted |  -  |
**404** | Message not found |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_languages**
> List[str] get_languages()

Get a list of all available languages

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
    api_instance = gbs3api.ApplicationInfoApi(api_client)

    try:
        # Get a list of all available languages
        api_response = api_instance.get_languages()
        print("The response of ApplicationInfoApi->get_languages:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling ApplicationInfoApi->get_languages: %s\n" % e)
```



### Parameters

This endpoint does not need any parameter.

### Return type

**List[str]**

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | All applications |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_messages**
> Dict[str, Dict[str, str]] get_messages(module=module, language=language, accept_language=accept_language)

Get the messages for the specified application and languages; Gets language from header if none specified

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
    api_instance = gbs3api.ApplicationInfoApi(api_client)
    module = ['module_example'] # List[str] | The modules to get the languages for (optional)
    language = ['language_example'] # List[str] | The languages to query for as an ISO 639 two letter language code (optional)
    accept_language = 'accept_language_example' # str | The language specified by the 'Accept-Language' HTTP header. Used if language list is empty (optional)

    try:
        # Get the messages for the specified application and languages; Gets language from header if none specified
        api_response = api_instance.get_messages(module=module, language=language, accept_language=accept_language)
        print("The response of ApplicationInfoApi->get_messages:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling ApplicationInfoApi->get_messages: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **module** | [**List[str]**](str.md)| The modules to get the languages for | [optional] 
 **language** | [**List[str]**](str.md)| The languages to query for as an ISO 639 two letter language code | [optional] 
 **accept_language** | **str**| The language specified by the &#39;Accept-Language&#39; HTTP header. Used if language list is empty | [optional] 

### Return type

**Dict[str, Dict[str, str]]**

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Application found; returning messages |  -  |
**404** | Application/Language not found - see body |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_modules**
> List[str] get_modules()

Get a list of all available modules

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
    api_instance = gbs3api.ApplicationInfoApi(api_client)

    try:
        # Get a list of all available modules
        api_response = api_instance.get_modules()
        print("The response of ApplicationInfoApi->get_modules:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling ApplicationInfoApi->get_modules: %s\n" % e)
```



### Parameters

This endpoint does not need any parameter.

### Return type

**List[str]**

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | All applications |  -  |
**404** | Application not found |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **save_messages**
> save_messages(module, request_body=request_body)

Create or update messages

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
    api_instance = gbs3api.ApplicationInfoApi(api_client)
    module = 'module_example' # str | The module to assign the messages to
    request_body = None # Dict[str, Dict[str, str]] | The messages, split by their languages and keys (optional)

    try:
        # Create or update messages
        api_instance.save_messages(module, request_body=request_body)
    except Exception as e:
        print("Exception when calling ApplicationInfoApi->save_messages: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **module** | **str**| The module to assign the messages to | 
 **request_body** | [**Dict[str, Dict[str, str]]**](Dict.md)| The messages, split by their languages and keys | [optional] 

### Return type

void (empty response body)

### Authorization

[APIKeyV1](../README.md#APIKeyV1), [CredentialsParameter](../README.md#CredentialsParameter), [BasicAuth](../README.md#BasicAuth), [JWTCookie](../README.md#JWTCookie), [JWT](../README.md#JWT)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: Not defined

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Successful |  -  |
**404** | Module/Language not found |  -  |
**400** | Bad request |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

