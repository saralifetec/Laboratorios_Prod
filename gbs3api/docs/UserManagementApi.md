# gbs3api.UserManagementApi

All URIs are relative to */GBS*

Method | HTTP request | Description
------------- | ------------- | -------------
[**get_group_roles**](UserManagementApi.md#get_group_roles) | **GET** /webservice/usermgmt/roles | 
[**get_person_info**](UserManagementApi.md#get_person_info) | **GET** /webservice/usermgmt/personInfo | 
[**get_persons**](UserManagementApi.md#get_persons) | **GET** /webservice/usermgmt/persons | 
[**get_user**](UserManagementApi.md#get_user) | **GET** /webservice/usermgmt/userinfo | 
[**get_user_groups**](UserManagementApi.md#get_user_groups) | **GET** /webservice/usermgmt/groups | 
[**get_users**](UserManagementApi.md#get_users) | **GET** /webservice/usermgmt/users | 


# **get_group_roles**
> get_group_roles(group=group)

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
    api_instance = gbs3api.UserManagementApi(api_client)
    group = 'group_example' # str |  (optional)

    try:
        api_instance.get_group_roles(group=group)
    except Exception as e:
        print("Exception when calling UserManagementApi->get_group_roles: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **group** | **str**|  | [optional] 

### Return type

void (empty response body)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json, application/xml

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**0** | default response |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_person_info**
> get_person_info(username=username)

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
    api_instance = gbs3api.UserManagementApi(api_client)
    username = 'username_example' # str |  (optional)

    try:
        api_instance.get_person_info(username=username)
    except Exception as e:
        print("Exception when calling UserManagementApi->get_person_info: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **username** | **str**|  | [optional] 

### Return type

void (empty response body)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json, application/xml

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**0** | default response |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_persons**
> get_persons(username=username)

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
    api_instance = gbs3api.UserManagementApi(api_client)
    username = 'username_example' # str |  (optional)

    try:
        api_instance.get_persons(username=username)
    except Exception as e:
        print("Exception when calling UserManagementApi->get_persons: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **username** | **str**|  | [optional] 

### Return type

void (empty response body)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json, application/xml

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**0** | default response |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_user**
> get_user(username=username)

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
    api_instance = gbs3api.UserManagementApi(api_client)
    username = 'username_example' # str |  (optional)

    try:
        api_instance.get_user(username=username)
    except Exception as e:
        print("Exception when calling UserManagementApi->get_user: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **username** | **str**|  | [optional] 

### Return type

void (empty response body)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json, application/xml

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**0** | default response |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_user_groups**
> get_user_groups(username=username)

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
    api_instance = gbs3api.UserManagementApi(api_client)
    username = 'username_example' # str |  (optional)

    try:
        api_instance.get_user_groups(username=username)
    except Exception as e:
        print("Exception when calling UserManagementApi->get_user_groups: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **username** | **str**|  | [optional] 

### Return type

void (empty response body)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json, application/xml

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**0** | default response |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_users**
> get_users(group=group)

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
    api_instance = gbs3api.UserManagementApi(api_client)
    group = 'group_example' # str |  (optional)

    try:
        api_instance.get_users(group=group)
    except Exception as e:
        print("Exception when calling UserManagementApi->get_users: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **group** | **str**|  | [optional] 

### Return type

void (empty response body)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json, application/xml

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**0** | default response |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

