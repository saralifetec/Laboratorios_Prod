# gbs4api.MasterDataControllerApi

All URIs are relative to *https://alfpwin0044.corp.passivesafety.com/gbs4-api*

Method | HTTP request | Description
------------- | ------------- | -------------
[**find_customers**](MasterDataControllerApi.md#find_customers) | **GET** /api/v1/master-data/customers | 
[**get_laboratories**](MasterDataControllerApi.md#get_laboratories) | **GET** /api/v1/master-data/laboratories | 
[**get_person_by_username**](MasterDataControllerApi.md#get_person_by_username) | **GET** /api/v1/master-data/persons/{username} | 
[**get_persons**](MasterDataControllerApi.md#get_persons) | **GET** /api/v1/master-data/persons | 
[**get_sub_test_types**](MasterDataControllerApi.md#get_sub_test_types) | **GET** /api/v1/master-data/test-types/{testTypeName}/sub-test-types | 
[**get_test_types**](MasterDataControllerApi.md#get_test_types) | **GET** /api/v1/master-data/test-types | 
[**get_vehicle_types_for_customer**](MasterDataControllerApi.md#get_vehicle_types_for_customer) | **GET** /api/v1/master-data/customers/{customerName}/vehicle-types | 


# **find_customers**
> List[CustomerDto] find_customers(filter=filter)

### Example


```python
import gbs4api
from gbs4api.models.customer_dto import CustomerDto
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
    api_instance = gbs4api.MasterDataControllerApi(api_client)
    filter = 'filter_example' # str |  (optional)

    try:
        api_response = api_instance.find_customers(filter=filter)
        print("The response of MasterDataControllerApi->find_customers:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling MasterDataControllerApi->find_customers: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **filter** | **str**|  | [optional] 

### Return type

[**List[CustomerDto]**](CustomerDto.md)

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

# **get_laboratories**
> List[LocationDto] get_laboratories()

### Example


```python
import gbs4api
from gbs4api.models.location_dto import LocationDto
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
    api_instance = gbs4api.MasterDataControllerApi(api_client)

    try:
        api_response = api_instance.get_laboratories()
        print("The response of MasterDataControllerApi->get_laboratories:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling MasterDataControllerApi->get_laboratories: %s\n" % e)
```



### Parameters

This endpoint does not need any parameter.

### Return type

[**List[LocationDto]**](LocationDto.md)

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

# **get_person_by_username**
> PersonDto get_person_by_username(username)

### Example


```python
import gbs4api
from gbs4api.models.person_dto import PersonDto
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
    api_instance = gbs4api.MasterDataControllerApi(api_client)
    username = 'username_example' # str | 

    try:
        api_response = api_instance.get_person_by_username(username)
        print("The response of MasterDataControllerApi->get_person_by_username:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling MasterDataControllerApi->get_person_by_username: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **username** | **str**|  | 

### Return type

[**PersonDto**](PersonDto.md)

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

# **get_persons**
> List[PersonDto] get_persons()

### Example


```python
import gbs4api
from gbs4api.models.person_dto import PersonDto
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
    api_instance = gbs4api.MasterDataControllerApi(api_client)

    try:
        api_response = api_instance.get_persons()
        print("The response of MasterDataControllerApi->get_persons:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling MasterDataControllerApi->get_persons: %s\n" % e)
```



### Parameters

This endpoint does not need any parameter.

### Return type

[**List[PersonDto]**](PersonDto.md)

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

# **get_sub_test_types**
> List[SubTestTypeDto] get_sub_test_types(test_type_name)

### Example


```python
import gbs4api
from gbs4api.models.sub_test_type_dto import SubTestTypeDto
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
    api_instance = gbs4api.MasterDataControllerApi(api_client)
    test_type_name = 'test_type_name_example' # str | 

    try:
        api_response = api_instance.get_sub_test_types(test_type_name)
        print("The response of MasterDataControllerApi->get_sub_test_types:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling MasterDataControllerApi->get_sub_test_types: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **test_type_name** | **str**|  | 

### Return type

[**List[SubTestTypeDto]**](SubTestTypeDto.md)

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

# **get_test_types**
> List[TestTypeDto] get_test_types()

### Example


```python
import gbs4api
from gbs4api.models.test_type_dto import TestTypeDto
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
    api_instance = gbs4api.MasterDataControllerApi(api_client)

    try:
        api_response = api_instance.get_test_types()
        print("The response of MasterDataControllerApi->get_test_types:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling MasterDataControllerApi->get_test_types: %s\n" % e)
```



### Parameters

This endpoint does not need any parameter.

### Return type

[**List[TestTypeDto]**](TestTypeDto.md)

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

# **get_vehicle_types_for_customer**
> List[VehicleTypeDto] get_vehicle_types_for_customer(customer_name)

### Example


```python
import gbs4api
from gbs4api.models.vehicle_type_dto import VehicleTypeDto
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
    api_instance = gbs4api.MasterDataControllerApi(api_client)
    customer_name = 'customer_name_example' # str | 

    try:
        api_response = api_instance.get_vehicle_types_for_customer(customer_name)
        print("The response of MasterDataControllerApi->get_vehicle_types_for_customer:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling MasterDataControllerApi->get_vehicle_types_for_customer: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **customer_name** | **str**|  | 

### Return type

[**List[VehicleTypeDto]**](VehicleTypeDto.md)

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

