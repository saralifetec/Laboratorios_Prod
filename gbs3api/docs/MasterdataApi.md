# gbs3api.MasterdataApi

All URIs are relative to */GBS*

Method | HTTP request | Description
------------- | ------------- | -------------
[**create_location**](MasterdataApi.md#create_location) | **POST** /webservice/master-data/locations | Create a new location
[**get_customer**](MasterdataApi.md#get_customer) | **GET** /webservice/master-data/customers/{customerName} | Find a customer by their name
[**get_customers**](MasterdataApi.md#get_customers) | **GET** /webservice/master-data/customers | Get all customers
[**get_location**](MasterdataApi.md#get_location) | **GET** /webservice/master-data/locations/{id} | Find a location by its id
[**get_locations**](MasterdataApi.md#get_locations) | **GET** /webservice/master-data/locations | Get locations based on different criteria
[**get_person**](MasterdataApi.md#get_person) | **GET** /webservice/master-data/persons/{id} | Find a person by their id
[**get_persons1**](MasterdataApi.md#get_persons1) | **GET** /webservice/master-data/persons | Get a person either by a specific username or all persons if no parameters present
[**get_sub_test_types**](MasterdataApi.md#get_sub_test_types) | **GET** /webservice/master-data/sub-test-types | Get all test sub types
[**get_team**](MasterdataApi.md#get_team) | **GET** /webservice/master-data/teams/{id} | Find a team by its id
[**get_teams**](MasterdataApi.md#get_teams) | **GET** /webservice/master-data/teams | Get all teams the authenticated user is part of
[**get_test_types**](MasterdataApi.md#get_test_types) | **GET** /webservice/master-data/test-types | Get all test types
[**get_vehicle_type_for_customer_by_name**](MasterdataApi.md#get_vehicle_type_for_customer_by_name) | **GET** /webservice/master-data/customers/{customerName}/vehicle-types/{vehicleTypeName} | Get a vehicle type by its name and that of its customer
[**get_vehicle_types**](MasterdataApi.md#get_vehicle_types) | **GET** /webservice/master-data/vehicle-types | Get all vehicle types
[**get_vehicle_types_for_customer**](MasterdataApi.md#get_vehicle_types_for_customer) | **GET** /webservice/master-data/customers/{customerName}/vehicle-types | Get all vehicle types for a customer
[**update_location**](MasterdataApi.md#update_location) | **PUT** /webservice/master-data/locations/{id} | Update a location


# **create_location**
> LocationDto create_location(location_dto=location_dto)

Create a new location

### Example

* Api Key Authentication (APIKeyV1):
* Api Key Authentication (CredentialsParameter):
* Basic Authentication (BasicAuth):
* Api Key Authentication (JWTCookie):
* Bearer (JWT) Authentication (JWT):

```python
import gbs3api
from gbs3api.models.location_dto import LocationDto
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
    api_instance = gbs3api.MasterdataApi(api_client)
    location_dto = gbs3api.LocationDto() # LocationDto |  (optional)

    try:
        # Create a new location
        api_response = api_instance.create_location(location_dto=location_dto)
        print("The response of MasterdataApi->create_location:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling MasterdataApi->create_location: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **location_dto** | [**LocationDto**](LocationDto.md)|  | [optional] 

### Return type

[**LocationDto**](LocationDto.md)

### Authorization

[APIKeyV1](../README.md#APIKeyV1), [CredentialsParameter](../README.md#CredentialsParameter), [BasicAuth](../README.md#BasicAuth), [JWTCookie](../README.md#JWTCookie), [JWT](../README.md#JWT)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**201** | Created |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_customer**
> CustomerDto get_customer(customer_name)

Find a customer by their name

### Example

* Api Key Authentication (APIKeyV1):
* Api Key Authentication (CredentialsParameter):
* Basic Authentication (BasicAuth):
* Api Key Authentication (JWTCookie):
* Bearer (JWT) Authentication (JWT):

```python
import gbs3api
from gbs3api.models.customer_dto import CustomerDto
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
    api_instance = gbs3api.MasterdataApi(api_client)
    customer_name = 'customer_name_example' # str | The ID of the customer

    try:
        # Find a customer by their name
        api_response = api_instance.get_customer(customer_name)
        print("The response of MasterdataApi->get_customer:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling MasterdataApi->get_customer: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **customer_name** | **str**| The ID of the customer | 

### Return type

[**CustomerDto**](CustomerDto.md)

### Authorization

[APIKeyV1](../README.md#APIKeyV1), [CredentialsParameter](../README.md#CredentialsParameter), [BasicAuth](../README.md#BasicAuth), [JWTCookie](../README.md#JWTCookie), [JWT](../README.md#JWT)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Customer found |  -  |
**404** | Customer not found |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_customers**
> List[CustomerDto] get_customers()

Get all customers

### Example

* Api Key Authentication (APIKeyV1):
* Api Key Authentication (CredentialsParameter):
* Basic Authentication (BasicAuth):
* Api Key Authentication (JWTCookie):
* Bearer (JWT) Authentication (JWT):

```python
import gbs3api
from gbs3api.models.customer_dto import CustomerDto
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
    api_instance = gbs3api.MasterdataApi(api_client)

    try:
        # Get all customers
        api_response = api_instance.get_customers()
        print("The response of MasterdataApi->get_customers:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling MasterdataApi->get_customers: %s\n" % e)
```



### Parameters

This endpoint does not need any parameter.

### Return type

[**List[CustomerDto]**](CustomerDto.md)

### Authorization

[APIKeyV1](../README.md#APIKeyV1), [CredentialsParameter](../README.md#CredentialsParameter), [BasicAuth](../README.md#BasicAuth), [JWTCookie](../README.md#JWTCookie), [JWT](../README.md#JWT)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | All found customers |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_location**
> LocationDto get_location(id)

Find a location by its id

### Example

* Api Key Authentication (APIKeyV1):
* Api Key Authentication (CredentialsParameter):
* Basic Authentication (BasicAuth):
* Api Key Authentication (JWTCookie):
* Bearer (JWT) Authentication (JWT):

```python
import gbs3api
from gbs3api.models.location_dto import LocationDto
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
    api_instance = gbs3api.MasterdataApi(api_client)
    id = 56 # int | The ID of the location

    try:
        # Find a location by its id
        api_response = api_instance.get_location(id)
        print("The response of MasterdataApi->get_location:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling MasterdataApi->get_location: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **int**| The ID of the location | 

### Return type

[**LocationDto**](LocationDto.md)

### Authorization

[APIKeyV1](../README.md#APIKeyV1), [CredentialsParameter](../README.md#CredentialsParameter), [BasicAuth](../README.md#BasicAuth), [JWTCookie](../README.md#JWTCookie), [JWT](../README.md#JWT)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Location found |  -  |
**404** | Location not found |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_locations**
> List[LocationDto] get_locations(label=label, location_category=location_category, event_id=event_id)

Get locations based on different criteria

### Example

* Api Key Authentication (APIKeyV1):
* Api Key Authentication (CredentialsParameter):
* Basic Authentication (BasicAuth):
* Api Key Authentication (JWTCookie):
* Bearer (JWT) Authentication (JWT):

```python
import gbs3api
from gbs3api.models.location_dto import LocationDto
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
    api_instance = gbs3api.MasterdataApi(api_client)
    label = 'label_example' # str | The label of the location; Cannot be combined with any other parameter (optional)
    location_category = 'location_category_example' # str | The category of the locations to find (optional)
    event_id = [56] # List[int] | A list of event ids; Returns all locations said events can be moved to; Cannot be combined with other parameters (optional)

    try:
        # Get locations based on different criteria
        api_response = api_instance.get_locations(label=label, location_category=location_category, event_id=event_id)
        print("The response of MasterdataApi->get_locations:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling MasterdataApi->get_locations: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **label** | **str**| The label of the location; Cannot be combined with any other parameter | [optional] 
 **location_category** | **str**| The category of the locations to find | [optional] 
 **event_id** | [**List[int]**](int.md)| A list of event ids; Returns all locations said events can be moved to; Cannot be combined with other parameters | [optional] 

### Return type

[**List[LocationDto]**](LocationDto.md)

### Authorization

[APIKeyV1](../README.md#APIKeyV1), [CredentialsParameter](../README.md#CredentialsParameter), [BasicAuth](../README.md#BasicAuth), [JWTCookie](../README.md#JWTCookie), [JWT](../README.md#JWT)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | All found locations |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_person**
> PersonDto get_person(id)

Find a person by their id

### Example

* Api Key Authentication (APIKeyV1):
* Api Key Authentication (CredentialsParameter):
* Basic Authentication (BasicAuth):
* Api Key Authentication (JWTCookie):
* Bearer (JWT) Authentication (JWT):

```python
import gbs3api
from gbs3api.models.person_dto import PersonDto
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
    api_instance = gbs3api.MasterdataApi(api_client)
    id = 56 # int | The ID of the person

    try:
        # Find a person by their id
        api_response = api_instance.get_person(id)
        print("The response of MasterdataApi->get_person:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling MasterdataApi->get_person: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **int**| The ID of the person | 

### Return type

[**PersonDto**](PersonDto.md)

### Authorization

[APIKeyV1](../README.md#APIKeyV1), [CredentialsParameter](../README.md#CredentialsParameter), [BasicAuth](../README.md#BasicAuth), [JWTCookie](../README.md#JWTCookie), [JWT](../README.md#JWT)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Person found |  -  |
**404** | Location not found |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_persons1**
> List[PersonDto] get_persons1(username=username)

Get a person either by a specific username or all persons if no parameters present

### Example

* Api Key Authentication (APIKeyV1):
* Api Key Authentication (CredentialsParameter):
* Basic Authentication (BasicAuth):
* Api Key Authentication (JWTCookie):
* Bearer (JWT) Authentication (JWT):

```python
import gbs3api
from gbs3api.models.person_dto import PersonDto
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
    api_instance = gbs3api.MasterdataApi(api_client)
    username = 'username_example' # str |  (optional)

    try:
        # Get a person either by a specific username or all persons if no parameters present
        api_response = api_instance.get_persons1(username=username)
        print("The response of MasterdataApi->get_persons1:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling MasterdataApi->get_persons1: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **username** | **str**|  | [optional] 

### Return type

[**List[PersonDto]**](PersonDto.md)

### Authorization

[APIKeyV1](../README.md#APIKeyV1), [CredentialsParameter](../README.md#CredentialsParameter), [BasicAuth](../README.md#BasicAuth), [JWTCookie](../README.md#JWTCookie), [JWT](../README.md#JWT)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | All found persons |  -  |
**400** | Not found |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_sub_test_types**
> List[SubTestTypeDto] get_sub_test_types()

Get all test sub types

### Example

* Api Key Authentication (APIKeyV1):
* Api Key Authentication (CredentialsParameter):
* Basic Authentication (BasicAuth):
* Api Key Authentication (JWTCookie):
* Bearer (JWT) Authentication (JWT):

```python
import gbs3api
from gbs3api.models.sub_test_type_dto import SubTestTypeDto
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
    api_instance = gbs3api.MasterdataApi(api_client)

    try:
        # Get all test sub types
        api_response = api_instance.get_sub_test_types()
        print("The response of MasterdataApi->get_sub_test_types:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling MasterdataApi->get_sub_test_types: %s\n" % e)
```



### Parameters

This endpoint does not need any parameter.

### Return type

[**List[SubTestTypeDto]**](SubTestTypeDto.md)

### Authorization

[APIKeyV1](../README.md#APIKeyV1), [CredentialsParameter](../README.md#CredentialsParameter), [BasicAuth](../README.md#BasicAuth), [JWTCookie](../README.md#JWTCookie), [JWT](../README.md#JWT)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | All found vehicle types |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_team**
> TeamDto get_team(id)

Find a team by its id

### Example

* Api Key Authentication (APIKeyV1):
* Api Key Authentication (CredentialsParameter):
* Basic Authentication (BasicAuth):
* Api Key Authentication (JWTCookie):
* Bearer (JWT) Authentication (JWT):

```python
import gbs3api
from gbs3api.models.team_dto import TeamDto
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
    api_instance = gbs3api.MasterdataApi(api_client)
    id = 56 # int | The ID of the team

    try:
        # Find a team by its id
        api_response = api_instance.get_team(id)
        print("The response of MasterdataApi->get_team:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling MasterdataApi->get_team: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **int**| The ID of the team | 

### Return type

[**TeamDto**](TeamDto.md)

### Authorization

[APIKeyV1](../README.md#APIKeyV1), [CredentialsParameter](../README.md#CredentialsParameter), [BasicAuth](../README.md#BasicAuth), [JWTCookie](../README.md#JWTCookie), [JWT](../README.md#JWT)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Team found |  -  |
**404** | Team not found |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_teams**
> List[TeamDto] get_teams()

Get all teams the authenticated user is part of

### Example

* Api Key Authentication (APIKeyV1):
* Api Key Authentication (CredentialsParameter):
* Basic Authentication (BasicAuth):
* Api Key Authentication (JWTCookie):
* Bearer (JWT) Authentication (JWT):

```python
import gbs3api
from gbs3api.models.team_dto import TeamDto
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
    api_instance = gbs3api.MasterdataApi(api_client)

    try:
        # Get all teams the authenticated user is part of
        api_response = api_instance.get_teams()
        print("The response of MasterdataApi->get_teams:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling MasterdataApi->get_teams: %s\n" % e)
```



### Parameters

This endpoint does not need any parameter.

### Return type

[**List[TeamDto]**](TeamDto.md)

### Authorization

[APIKeyV1](../README.md#APIKeyV1), [CredentialsParameter](../README.md#CredentialsParameter), [BasicAuth](../README.md#BasicAuth), [JWTCookie](../README.md#JWTCookie), [JWT](../README.md#JWT)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | All found teams |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_test_types**
> List[TestTypeDto] get_test_types()

Get all test types

### Example

* Api Key Authentication (APIKeyV1):
* Api Key Authentication (CredentialsParameter):
* Basic Authentication (BasicAuth):
* Api Key Authentication (JWTCookie):
* Bearer (JWT) Authentication (JWT):

```python
import gbs3api
from gbs3api.models.test_type_dto import TestTypeDto
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
    api_instance = gbs3api.MasterdataApi(api_client)

    try:
        # Get all test types
        api_response = api_instance.get_test_types()
        print("The response of MasterdataApi->get_test_types:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling MasterdataApi->get_test_types: %s\n" % e)
```



### Parameters

This endpoint does not need any parameter.

### Return type

[**List[TestTypeDto]**](TestTypeDto.md)

### Authorization

[APIKeyV1](../README.md#APIKeyV1), [CredentialsParameter](../README.md#CredentialsParameter), [BasicAuth](../README.md#BasicAuth), [JWTCookie](../README.md#JWTCookie), [JWT](../README.md#JWT)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | All test types |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_vehicle_type_for_customer_by_name**
> List[VehicleTypeDto] get_vehicle_type_for_customer_by_name(customer_name, vehicle_type_name)

Get a vehicle type by its name and that of its customer

### Example

* Api Key Authentication (APIKeyV1):
* Api Key Authentication (CredentialsParameter):
* Basic Authentication (BasicAuth):
* Api Key Authentication (JWTCookie):
* Bearer (JWT) Authentication (JWT):

```python
import gbs3api
from gbs3api.models.vehicle_type_dto import VehicleTypeDto
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
    api_instance = gbs3api.MasterdataApi(api_client)
    customer_name = 'customer_name_example' # str | The name of the vehicle type's producer
    vehicle_type_name = 'vehicle_type_name_example' # str | The name of the vehicle type

    try:
        # Get a vehicle type by its name and that of its customer
        api_response = api_instance.get_vehicle_type_for_customer_by_name(customer_name, vehicle_type_name)
        print("The response of MasterdataApi->get_vehicle_type_for_customer_by_name:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling MasterdataApi->get_vehicle_type_for_customer_by_name: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **customer_name** | **str**| The name of the vehicle type&#39;s producer | 
 **vehicle_type_name** | **str**| The name of the vehicle type | 

### Return type

[**List[VehicleTypeDto]**](VehicleTypeDto.md)

### Authorization

[APIKeyV1](../README.md#APIKeyV1), [CredentialsParameter](../README.md#CredentialsParameter), [BasicAuth](../README.md#BasicAuth), [JWTCookie](../README.md#JWTCookie), [JWT](../README.md#JWT)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | The found vehicle type |  -  |
**400** | Vehicle type/customer not found |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_vehicle_types**
> List[VehicleTypeDto] get_vehicle_types()

Get all vehicle types

### Example

* Api Key Authentication (APIKeyV1):
* Api Key Authentication (CredentialsParameter):
* Basic Authentication (BasicAuth):
* Api Key Authentication (JWTCookie):
* Bearer (JWT) Authentication (JWT):

```python
import gbs3api
from gbs3api.models.vehicle_type_dto import VehicleTypeDto
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
    api_instance = gbs3api.MasterdataApi(api_client)

    try:
        # Get all vehicle types
        api_response = api_instance.get_vehicle_types()
        print("The response of MasterdataApi->get_vehicle_types:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling MasterdataApi->get_vehicle_types: %s\n" % e)
```



### Parameters

This endpoint does not need any parameter.

### Return type

[**List[VehicleTypeDto]**](VehicleTypeDto.md)

### Authorization

[APIKeyV1](../README.md#APIKeyV1), [CredentialsParameter](../README.md#CredentialsParameter), [BasicAuth](../README.md#BasicAuth), [JWTCookie](../README.md#JWTCookie), [JWT](../README.md#JWT)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | All found vehicle types |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_vehicle_types_for_customer**
> List[VehicleTypeDto] get_vehicle_types_for_customer(customer_name)

Get all vehicle types for a customer

### Example

* Api Key Authentication (APIKeyV1):
* Api Key Authentication (CredentialsParameter):
* Basic Authentication (BasicAuth):
* Api Key Authentication (JWTCookie):
* Bearer (JWT) Authentication (JWT):

```python
import gbs3api
from gbs3api.models.vehicle_type_dto import VehicleTypeDto
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
    api_instance = gbs3api.MasterdataApi(api_client)
    customer_name = 'customer_name_example' # str | The name of the vehicle type's producer

    try:
        # Get all vehicle types for a customer
        api_response = api_instance.get_vehicle_types_for_customer(customer_name)
        print("The response of MasterdataApi->get_vehicle_types_for_customer:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling MasterdataApi->get_vehicle_types_for_customer: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **customer_name** | **str**| The name of the vehicle type&#39;s producer | 

### Return type

[**List[VehicleTypeDto]**](VehicleTypeDto.md)

### Authorization

[APIKeyV1](../README.md#APIKeyV1), [CredentialsParameter](../README.md#CredentialsParameter), [BasicAuth](../README.md#BasicAuth), [JWTCookie](../README.md#JWTCookie), [JWT](../README.md#JWT)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | All found vehicle types |  -  |
**400** | Customer not found |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **update_location**
> update_location(id, location_dto=location_dto)

Update a location

### Example

* Api Key Authentication (APIKeyV1):
* Api Key Authentication (CredentialsParameter):
* Basic Authentication (BasicAuth):
* Api Key Authentication (JWTCookie):
* Bearer (JWT) Authentication (JWT):

```python
import gbs3api
from gbs3api.models.location_dto import LocationDto
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
    api_instance = gbs3api.MasterdataApi(api_client)
    id = 56 # int | 
    location_dto = gbs3api.LocationDto() # LocationDto |  (optional)

    try:
        # Update a location
        api_instance.update_location(id, location_dto=location_dto)
    except Exception as e:
        print("Exception when calling MasterdataApi->update_location: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **int**|  | 
 **location_dto** | [**LocationDto**](LocationDto.md)|  | [optional] 

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
**204** | Updated |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

