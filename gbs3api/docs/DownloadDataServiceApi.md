# gbs3api.DownloadDataServiceApi

All URIs are relative to */GBS*

Method | HTTP request | Description
------------- | ------------- | -------------
[**download_data**](DownloadDataServiceApi.md#download_data) | **GET** /webservice/download-data/additionalvalue/{additionalvalueId} | Download a data by its ID


# **download_data**
> download_data(additionalvalue_id, datatype=datatype, query_param_apikey=query_param_apikey)

Download a data by its ID

Streams the data as an attachment.

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
    api_instance = gbs3api.DownloadDataServiceApi(api_client)
    additionalvalue_id = 56 # int | The ID of the Additional value
    datatype = 'datatype_example' # str |  (optional)
    query_param_apikey = 'query_param_apikey_example' # str |  (optional)

    try:
        # Download a data by its ID
        api_instance.download_data(additionalvalue_id, datatype=datatype, query_param_apikey=query_param_apikey)
    except Exception as e:
        print("Exception when calling DownloadDataServiceApi->download_data: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **additionalvalue_id** | **int**| The ID of the Additional value | 
 **datatype** | **str**|  | [optional] 
 **query_param_apikey** | **str**|  | [optional] 

### Return type

void (empty response body)

### Authorization

[APIKeyV1](../README.md#APIKeyV1), [CredentialsParameter](../README.md#CredentialsParameter), [BasicAuth](../README.md#BasicAuth), [JWTCookie](../README.md#JWTCookie), [JWT](../README.md#JWT)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/octet-stream

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Data downloaded successfully |  -  |
**400** | Bad request |  -  |
**404** | Data not found |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

