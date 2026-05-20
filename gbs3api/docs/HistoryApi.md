# gbs3api.HistoryApi

All URIs are relative to */GBS*

Method | HTTP request | Description
------------- | ------------- | -------------
[**get_logs**](HistoryApi.md#get_logs) | **GET** /webservice/history/logs | Get history log entries through different query parameters


# **get_logs**
> List[HistoryLog] get_logs(var_from=var_from, to=to, entity_id=entity_id, object_type=object_type, user=user)

Get history log entries through different query parameters

### Example

* Api Key Authentication (APIKeyV1):
* Api Key Authentication (CredentialsParameter):
* Basic Authentication (BasicAuth):
* Api Key Authentication (JWTCookie):
* Bearer (JWT) Authentication (JWT):

```python
import gbs3api
from gbs3api.models.history_log import HistoryLog
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
    api_instance = gbs3api.HistoryApi(api_client)
    var_from = 'var_from_example' # str | The from date to query; Formatted as yyyy-MM-ddTHH:mm:ss.SSSZ (optional)
    to = 'to_example' # str | The to date to query; yyyy-MM-ddTHH:mm:ss.SSSZ (optional)
    entity_id = 56 # int | Cannot be used together with objectType! The id of the entity to filter by (optional)
    object_type = 'object_type_example' # str | Cannot be used together with entityId! The type of object to filter by (optional)
    user = 'user_example' # str | The user to filter by (optional)

    try:
        # Get history log entries through different query parameters
        api_response = api_instance.get_logs(var_from=var_from, to=to, entity_id=entity_id, object_type=object_type, user=user)
        print("The response of HistoryApi->get_logs:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling HistoryApi->get_logs: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **var_from** | **str**| The from date to query; Formatted as yyyy-MM-ddTHH:mm:ss.SSSZ | [optional] 
 **to** | **str**| The to date to query; yyyy-MM-ddTHH:mm:ss.SSSZ | [optional] 
 **entity_id** | **int**| Cannot be used together with objectType! The id of the entity to filter by | [optional] 
 **object_type** | **str**| Cannot be used together with entityId! The type of object to filter by | [optional] 
 **user** | **str**| The user to filter by | [optional] 

### Return type

[**List[HistoryLog]**](HistoryLog.md)

### Authorization

[APIKeyV1](../README.md#APIKeyV1), [CredentialsParameter](../README.md#CredentialsParameter), [BasicAuth](../README.md#BasicAuth), [JWTCookie](../README.md#JWTCookie), [JWT](../README.md#JWT)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | All found entries; Ordered by date (newest first) |  -  |
**400** | Malformed request; Further information in response body |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

