# gbs3api.ReportDataSourcesApi

All URIs are relative to */GBS*

Method | HTTP request | Description
------------- | ------------- | -------------
[**get_additional_groups_for_series**](ReportDataSourcesApi.md#get_additional_groups_for_series) | **GET** /webservice/additional-groups/series/{seriesId} | Retrieve test data by seriesId and vpnrPos (TestStep position No.)
[**get_additional_groups_for_series1**](ReportDataSourcesApi.md#get_additional_groups_for_series1) | **GET** /webservice/additional-groups-and-series/series/{seriesId} | Retrieve a ... by its seriesId and vpnrPos (TestStep position No.)
[**get_additional_groups_for_series2**](ReportDataSourcesApi.md#get_additional_groups_for_series2) | **GET** /webservice/general-book-data/series/{seriesId} | Retrieve a ... by its seriesId and vpnrPos (TestStep position No.)
[**get_additional_groups_for_test**](ReportDataSourcesApi.md#get_additional_groups_for_test) | **GET** /webservice/additional-groups/tests/{testId} | Retrieve a ... by its seriesId and vpnrPos (TestStep position No.)
[**get_additional_groups_for_test1**](ReportDataSourcesApi.md#get_additional_groups_for_test1) | **GET** /webservice/additional-groups/tests | Retrieve a test data by test ids and vpnrPos (TestStep position No.)
[**get_additional_groups_for_test2**](ReportDataSourcesApi.md#get_additional_groups_for_test2) | **GET** /webservice/additional-groups-and-series/tests | Retrieve a test data and test series metadata by test ids
[**get_additional_groups_for_test3**](ReportDataSourcesApi.md#get_additional_groups_for_test3) | **GET** /webservice/general-book-data/tests | Retrieve a test data by test ids and vpnrPos (TestStep position No.), testseries data, parts data, GBS system instance data
[**get_boms_for_series**](ReportDataSourcesApi.md#get_boms_for_series) | **GET** /webservice/parts/boms/series/{seriesId} | Retrieve a bom by its Test series id
[**get_boms_for_test**](ReportDataSourcesApi.md#get_boms_for_test) | **GET** /webservice/parts/boms/tests/{testId} | Retrieve a Bom by its testId 
[**get_boms_for_test1**](ReportDataSourcesApi.md#get_boms_for_test1) | **GET** /webservice/parts/boms/tests | Retrieve a Bom by testIds
[**get_component_test_groups**](ReportDataSourcesApi.md#get_component_test_groups) | **GET** /webservice/component-matrix/component-groups/series/{seriesId} | Retrieve component group by its seriesId and active Tests
[**get_devices_for_series**](ReportDataSourcesApi.md#get_devices_for_series) | **GET** /webservice/devices/series/{seriesId} | Retrieve a device by its seriesId and vpnrPos (TestStep position No.)
[**get_devices_for_test**](ReportDataSourcesApi.md#get_devices_for_test) | **GET** /webservice/devices/tests/{testId} | Retrieve a device by its TestStep Id and vpnrPos (TestStep position No.)
[**get_gbs_instance**](ReportDataSourcesApi.md#get_gbs_instance) | **GET** /webservice/general-information/gbs-instance | Retrieve GBS Instance
[**get_get_component_matrix_test_steps**](ReportDataSourcesApi.md#get_get_component_matrix_test_steps) | **GET** /webservice/component-matrix/steps/series/{seriesId} | Retrieve Matrix TestSteps by its seriesId and active tests only and wrap to one node
[**get_parts_for_series**](ReportDataSourcesApi.md#get_parts_for_series) | **GET** /webservice/parts/series/{seriesId} | Retrieve parts by its seriesId
[**get_parts_for_test**](ReportDataSourcesApi.md#get_parts_for_test) | **GET** /webservice/parts/tests/{testId} | Retrieve parts by its test Id
[**get_parts_for_tests**](ReportDataSourcesApi.md#get_parts_for_tests) | **GET** /webservice/parts/tests | Retrieve parts by test Ids
[**get_test_series_summary**](ReportDataSourcesApi.md#get_test_series_summary) | **GET** /webservice/general-information/series/{seriesId} | Retrieve General Information by its seriesId
[**get_used_equipment_for_series**](ReportDataSourcesApi.md#get_used_equipment_for_series) | **GET** /webservice/equipment-devices/series/{seriesId} | Retrieve used equipment and devices by its seriesId and vpnrPos (TestStep position No.)
[**get_used_equipment_for_series1**](ReportDataSourcesApi.md#get_used_equipment_for_series1) | **GET** /webservice/used-equipment/series/{seriesId} | Retrieve used equipment by its seriesId and vpnrPos (TestStep position No.)
[**get_used_equipment_for_test**](ReportDataSourcesApi.md#get_used_equipment_for_test) | **GET** /webservice/used-equipment/tests/{testId} | Retrieve used equipment by its seriesId and vpnrPos (TestStep position No.)


# **get_additional_groups_for_series**
> TestSequenceDto get_additional_groups_for_series(series_id, category=category, region=region, vpnr_pos=vpnr_pos, flat_group_structure=flat_group_structure)

Retrieve test data by seriesId and vpnrPos (TestStep position No.)

Returns test data organized as a list of test sequences associated with specified test series. Each returned test sequence contains its metadata and hierarchical component structure (from testStep to additionals ). Particular endpoint: http://localhost:8083/GBS/webservice/additional-groups/series/86212392?vpnrPos=2&vpnrPos=5?category=SWS_COMPONENT_RESULT?flatGroupStructure=false

### Example

* Api Key Authentication (APIKeyV1):
* Api Key Authentication (CredentialsParameter):
* Basic Authentication (BasicAuth):
* Api Key Authentication (JWTCookie):
* Bearer (JWT) Authentication (JWT):

```python
import gbs3api
from gbs3api.models.test_sequence_dto import TestSequenceDto
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
    api_instance = gbs3api.ReportDataSourcesApi(api_client)
    series_id = 134235421 # int | Unique identifier of the Test Series (must be a numeric value)
    category = ['SWS_COMPONENT_RESULT'] # List[str] | Category of test data (parameter, result, requirement)  (optional)
    region = 'ENGLISH' # str | This is Region (optional)
    vpnr_pos = [1] # List[int] | This is in another words TestStep position No. Has to be >0 (optional)
    flat_group_structure = False # bool | Determines if child (nested ) additional groups should be displayed in response on one level with theirs parent additional groups. In GBS reports we resigned from this, as we need to present additional groups in hierarchy. By default value is false. (optional) (default to False)

    try:
        # Retrieve test data by seriesId and vpnrPos (TestStep position No.)
        api_response = api_instance.get_additional_groups_for_series(series_id, category=category, region=region, vpnr_pos=vpnr_pos, flat_group_structure=flat_group_structure)
        print("The response of ReportDataSourcesApi->get_additional_groups_for_series:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling ReportDataSourcesApi->get_additional_groups_for_series: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **series_id** | **int**| Unique identifier of the Test Series (must be a numeric value) | 
 **category** | [**List[str]**](str.md)| Category of test data (parameter, result, requirement)  | [optional] 
 **region** | **str**| This is Region | [optional] 
 **vpnr_pos** | [**List[int]**](int.md)| This is in another words TestStep position No. Has to be &gt;0 | [optional] 
 **flat_group_structure** | **bool**| Determines if child (nested ) additional groups should be displayed in response on one level with theirs parent additional groups. In GBS reports we resigned from this, as we need to present additional groups in hierarchy. By default value is false. | [optional] [default to False]

### Return type

[**TestSequenceDto**](TestSequenceDto.md)

### Authorization

[APIKeyV1](../README.md#APIKeyV1), [CredentialsParameter](../README.md#CredentialsParameter), [BasicAuth](../README.md#BasicAuth), [JWTCookie](../README.md#JWTCookie), [JWT](../README.md#JWT)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/xml, application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | ... retrieved successfully |  -  |
**400** | Invalid request, Test series id number needs to be provided and numeric. |  -  |
**500** | Internal server error |  -  |
**404** | Series ID or ... not found |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_additional_groups_for_series1**
> TestSequenceDto get_additional_groups_for_series1(series_id, category=category, vpnr_pos=vpnr_pos, flat_group_structure=flat_group_structure)

Retrieve a ... by its seriesId and vpnrPos (TestStep position No.)

### Example

* Api Key Authentication (APIKeyV1):
* Api Key Authentication (CredentialsParameter):
* Basic Authentication (BasicAuth):
* Api Key Authentication (JWTCookie):
* Bearer (JWT) Authentication (JWT):

```python
import gbs3api
from gbs3api.models.test_sequence_dto import TestSequenceDto
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
    api_instance = gbs3api.ReportDataSourcesApi(api_client)
    series_id = 56 # int | The ID of the series
    category = ['category_example'] # List[str] |  (optional)
    vpnr_pos = [56] # List[int] |  (optional)
    flat_group_structure = False # bool |  (optional) (default to False)

    try:
        # Retrieve a ... by its seriesId and vpnrPos (TestStep position No.)
        api_response = api_instance.get_additional_groups_for_series1(series_id, category=category, vpnr_pos=vpnr_pos, flat_group_structure=flat_group_structure)
        print("The response of ReportDataSourcesApi->get_additional_groups_for_series1:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling ReportDataSourcesApi->get_additional_groups_for_series1: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **series_id** | **int**| The ID of the series | 
 **category** | [**List[str]**](str.md)|  | [optional] 
 **vpnr_pos** | [**List[int]**](int.md)|  | [optional] 
 **flat_group_structure** | **bool**|  | [optional] [default to False]

### Return type

[**TestSequenceDto**](TestSequenceDto.md)

### Authorization

[APIKeyV1](../README.md#APIKeyV1), [CredentialsParameter](../README.md#CredentialsParameter), [BasicAuth](../README.md#BasicAuth), [JWTCookie](../README.md#JWTCookie), [JWT](../README.md#JWT)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json, application/xml

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | ... retrieved successfully |  -  |
**400** | Bad request, Test series id number needs to be present! |  -  |
**404** | Series ID or ... not found |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_additional_groups_for_series2**
> TestSequenceDto get_additional_groups_for_series2(series_id, category=category, vpnr_pos=vpnr_pos, test_ids=test_ids, flat_group_structure=flat_group_structure)

Retrieve a ... by its seriesId and vpnrPos (TestStep position No.)

### Example

* Api Key Authentication (APIKeyV1):
* Api Key Authentication (CredentialsParameter):
* Basic Authentication (BasicAuth):
* Api Key Authentication (JWTCookie):
* Bearer (JWT) Authentication (JWT):

```python
import gbs3api
from gbs3api.models.test_sequence_dto import TestSequenceDto
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
    api_instance = gbs3api.ReportDataSourcesApi(api_client)
    series_id = 56 # int | The ID of the series
    category = ['category_example'] # List[str] |  (optional)
    vpnr_pos = [56] # List[int] |  (optional)
    test_ids = [56] # List[int] |  (optional)
    flat_group_structure = False # bool |  (optional) (default to False)

    try:
        # Retrieve a ... by its seriesId and vpnrPos (TestStep position No.)
        api_response = api_instance.get_additional_groups_for_series2(series_id, category=category, vpnr_pos=vpnr_pos, test_ids=test_ids, flat_group_structure=flat_group_structure)
        print("The response of ReportDataSourcesApi->get_additional_groups_for_series2:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling ReportDataSourcesApi->get_additional_groups_for_series2: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **series_id** | **int**| The ID of the series | 
 **category** | [**List[str]**](str.md)|  | [optional] 
 **vpnr_pos** | [**List[int]**](int.md)|  | [optional] 
 **test_ids** | [**List[int]**](int.md)|  | [optional] 
 **flat_group_structure** | **bool**|  | [optional] [default to False]

### Return type

[**TestSequenceDto**](TestSequenceDto.md)

### Authorization

[APIKeyV1](../README.md#APIKeyV1), [CredentialsParameter](../README.md#CredentialsParameter), [BasicAuth](../README.md#BasicAuth), [JWTCookie](../README.md#JWTCookie), [JWT](../README.md#JWT)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json, application/xml

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | ... retrieved successfully |  -  |
**400** | Bad request, Test series id number needs to be present! |  -  |
**404** | Series ID or ... not found |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_additional_groups_for_test**
> TestSequenceDto get_additional_groups_for_test(test_id, category=category, region=region, vpnr_pos=vpnr_pos, flat_group_structure=flat_group_structure)

Retrieve a ... by its seriesId and vpnrPos (TestStep position No.)

### Example

* Api Key Authentication (APIKeyV1):
* Api Key Authentication (CredentialsParameter):
* Basic Authentication (BasicAuth):
* Api Key Authentication (JWTCookie):
* Bearer (JWT) Authentication (JWT):

```python
import gbs3api
from gbs3api.models.test_sequence_dto import TestSequenceDto
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
    api_instance = gbs3api.ReportDataSourcesApi(api_client)
    test_id = 56 # int | The ID of the one TestStep
    category = ['category_example'] # List[str] |  (optional)
    region = 'region_example' # str |  (optional)
    vpnr_pos = [56] # List[int] |  (optional)
    flat_group_structure = False # bool |  (optional) (default to False)

    try:
        # Retrieve a ... by its seriesId and vpnrPos (TestStep position No.)
        api_response = api_instance.get_additional_groups_for_test(test_id, category=category, region=region, vpnr_pos=vpnr_pos, flat_group_structure=flat_group_structure)
        print("The response of ReportDataSourcesApi->get_additional_groups_for_test:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling ReportDataSourcesApi->get_additional_groups_for_test: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **test_id** | **int**| The ID of the one TestStep | 
 **category** | [**List[str]**](str.md)|  | [optional] 
 **region** | **str**|  | [optional] 
 **vpnr_pos** | [**List[int]**](int.md)|  | [optional] 
 **flat_group_structure** | **bool**|  | [optional] [default to False]

### Return type

[**TestSequenceDto**](TestSequenceDto.md)

### Authorization

[APIKeyV1](../README.md#APIKeyV1), [CredentialsParameter](../README.md#CredentialsParameter), [BasicAuth](../README.md#BasicAuth), [JWTCookie](../README.md#JWTCookie), [JWT](../README.md#JWT)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | ... retrieved successfully |  -  |
**400** | Bad request, Test series id number needs to be present! |  -  |
**404** | Series ID or ... not found |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_additional_groups_for_test1**
> TestSequenceDto get_additional_groups_for_test1(test_ids, category=category, region=region, vpnr_pos=vpnr_pos, flat_group_structure=flat_group_structure)

Retrieve a test data by test ids and vpnrPos (TestStep position No.)

Returns test data organized as a list of test sequences associated with specified test ids. Each returned test sequence contains its metadata and hierarchical component structure (from testStep to additionals ). Particular endpoint: http://localhost:8083/GBS/webservice/additional-groups/tests?testIds=86215369&testIds=86214852&testIds=86213995?vpnrPos=1?category=SWS_COMPONENT_RESULT?flatGroupStructure=false

### Example

* Api Key Authentication (APIKeyV1):
* Api Key Authentication (CredentialsParameter):
* Basic Authentication (BasicAuth):
* Api Key Authentication (JWTCookie):
* Bearer (JWT) Authentication (JWT):

```python
import gbs3api
from gbs3api.models.test_sequence_dto import TestSequenceDto
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
    api_instance = gbs3api.ReportDataSourcesApi(api_client)
    test_ids = [86213995] # List[int] | Ids of tests
    category = ['SWS_COMPONENT_RESULT'] # List[str] | Category of test data (parameter, result, requirement)  (optional)
    region = 'ENGLISH' # str | This is Region (optional)
    vpnr_pos = [1] # List[int] | This is in another words TestStep position No. Has to be >0 (optional)
    flat_group_structure = False # bool | Determines if child (nested ) additional groups should be displayed in response on one level with theirs parent additional groups. In GBS reports we resigned from this, as we need to present additional groups in hierarchy. By default value is false. (optional) (default to False)

    try:
        # Retrieve a test data by test ids and vpnrPos (TestStep position No.)
        api_response = api_instance.get_additional_groups_for_test1(test_ids, category=category, region=region, vpnr_pos=vpnr_pos, flat_group_structure=flat_group_structure)
        print("The response of ReportDataSourcesApi->get_additional_groups_for_test1:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling ReportDataSourcesApi->get_additional_groups_for_test1: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **test_ids** | [**List[int]**](int.md)| Ids of tests | 
 **category** | [**List[str]**](str.md)| Category of test data (parameter, result, requirement)  | [optional] 
 **region** | **str**| This is Region | [optional] 
 **vpnr_pos** | [**List[int]**](int.md)| This is in another words TestStep position No. Has to be &gt;0 | [optional] 
 **flat_group_structure** | **bool**| Determines if child (nested ) additional groups should be displayed in response on one level with theirs parent additional groups. In GBS reports we resigned from this, as we need to present additional groups in hierarchy. By default value is false. | [optional] [default to False]

### Return type

[**TestSequenceDto**](TestSequenceDto.md)

### Authorization

[APIKeyV1](../README.md#APIKeyV1), [CredentialsParameter](../README.md#CredentialsParameter), [BasicAuth](../README.md#BasicAuth), [JWTCookie](../README.md#JWTCookie), [JWT](../README.md#JWT)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | ... retrieved successfully |  -  |
**400** | Bad request, Test  id number needs to be present! |  -  |
**500** | Internal server error |  -  |
**404** | Test ID not found |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_additional_groups_for_test2**
> TestSequenceDto get_additional_groups_for_test2(test_ids, category=category, vpnr_pos=vpnr_pos, flat_group_structure=flat_group_structure)

Retrieve a test data and test series metadata by test ids

Returns testseries metadata and test data organized as a list of test sequences associated with specified test ids. Each returned test sequence contains its metadata and hierarchical component structure (from testStep to additionals ). Particular endpoint: http://localhost:8083/GBS/webservice/additional-groups-and-series/tests?testIds=86215369&testIds=86214852&testIds=86213995

### Example

* Api Key Authentication (APIKeyV1):
* Api Key Authentication (CredentialsParameter):
* Basic Authentication (BasicAuth):
* Api Key Authentication (JWTCookie):
* Bearer (JWT) Authentication (JWT):

```python
import gbs3api
from gbs3api.models.test_sequence_dto import TestSequenceDto
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
    api_instance = gbs3api.ReportDataSourcesApi(api_client)
    test_ids = [86213995] # List[int] | Ids of tests
    category = ['SWS_COMPONENT_RESULT'] # List[str] | Category of test data (parameter, result, requirement)  (optional)
    vpnr_pos = [1] # List[int] | This is in another words TestStep position No. Has to be >0 (optional)
    flat_group_structure = False # bool | Determines if child (nested ) additional groups should be displayed in response on one level with theirs parent additional groups. In GBS reports we resigned from this, as we need to present additional groups in hierarchy. By default value is false. (optional) (default to False)

    try:
        # Retrieve a test data and test series metadata by test ids
        api_response = api_instance.get_additional_groups_for_test2(test_ids, category=category, vpnr_pos=vpnr_pos, flat_group_structure=flat_group_structure)
        print("The response of ReportDataSourcesApi->get_additional_groups_for_test2:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling ReportDataSourcesApi->get_additional_groups_for_test2: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **test_ids** | [**List[int]**](int.md)| Ids of tests | 
 **category** | [**List[str]**](str.md)| Category of test data (parameter, result, requirement)  | [optional] 
 **vpnr_pos** | [**List[int]**](int.md)| This is in another words TestStep position No. Has to be &gt;0 | [optional] 
 **flat_group_structure** | **bool**| Determines if child (nested ) additional groups should be displayed in response on one level with theirs parent additional groups. In GBS reports we resigned from this, as we need to present additional groups in hierarchy. By default value is false. | [optional] [default to False]

### Return type

[**TestSequenceDto**](TestSequenceDto.md)

### Authorization

[APIKeyV1](../README.md#APIKeyV1), [CredentialsParameter](../README.md#CredentialsParameter), [BasicAuth](../README.md#BasicAuth), [JWTCookie](../README.md#JWTCookie), [JWT](../README.md#JWT)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | ... retrieved successfully |  -  |
**400** | Bad request, Test  id number needs to be present! |  -  |
**500** | Internal server error |  -  |
**404** | Series ID or ... not found |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_additional_groups_for_test3**
> TestSequenceDto get_additional_groups_for_test3(test_ids, category=category, vpnr_pos=vpnr_pos, currently_logged_user=currently_logged_user, flat_group_structure=flat_group_structure)

Retrieve a test data by test ids and vpnrPos (TestStep position No.), testseries data, parts data, GBS system instance data

Returns test data organized as a list of test sequences associated with specified test ids. Each returned test sequence contains its metadata and hierarchical"
component structure (from testStep to additionals ). Beside of this it returns testseries data, parts data, GBS system instance data. Particular endpoint: http://localhost:8083/GBS/webservice/general-book-data/tests?testIds=86215369&testIds=86214852&testIds=86213995&currentlyLoggedUser=Tom%20Joad

### Example

* Api Key Authentication (APIKeyV1):
* Api Key Authentication (CredentialsParameter):
* Basic Authentication (BasicAuth):
* Api Key Authentication (JWTCookie):
* Bearer (JWT) Authentication (JWT):

```python
import gbs3api
from gbs3api.models.test_sequence_dto import TestSequenceDto
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
    api_instance = gbs3api.ReportDataSourcesApi(api_client)
    test_ids = [86213995] # List[int] | Ids of tests
    category = ['SWS_COMPONENT_RESULT'] # List[str] | Category of test data (parameter, result, requirement)  (optional)
    vpnr_pos = [1] # List[int] | This is in another words TestStep position No. Has to be >0 (optional)
    currently_logged_user = 'currently_logged_user_example' # str |  (optional)
    flat_group_structure = False # bool | Determines if child (nested ) additional groups should be displayed in response on one level with theirs parent additional groups. In GBS reports we resigned from this, as we need to present additional groups in hierarchy. By default value is false. (optional) (default to False)

    try:
        # Retrieve a test data by test ids and vpnrPos (TestStep position No.), testseries data, parts data, GBS system instance data
        api_response = api_instance.get_additional_groups_for_test3(test_ids, category=category, vpnr_pos=vpnr_pos, currently_logged_user=currently_logged_user, flat_group_structure=flat_group_structure)
        print("The response of ReportDataSourcesApi->get_additional_groups_for_test3:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling ReportDataSourcesApi->get_additional_groups_for_test3: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **test_ids** | [**List[int]**](int.md)| Ids of tests | 
 **category** | [**List[str]**](str.md)| Category of test data (parameter, result, requirement)  | [optional] 
 **vpnr_pos** | [**List[int]**](int.md)| This is in another words TestStep position No. Has to be &gt;0 | [optional] 
 **currently_logged_user** | **str**|  | [optional] 
 **flat_group_structure** | **bool**| Determines if child (nested ) additional groups should be displayed in response on one level with theirs parent additional groups. In GBS reports we resigned from this, as we need to present additional groups in hierarchy. By default value is false. | [optional] [default to False]

### Return type

[**TestSequenceDto**](TestSequenceDto.md)

### Authorization

[APIKeyV1](../README.md#APIKeyV1), [CredentialsParameter](../README.md#CredentialsParameter), [BasicAuth](../README.md#BasicAuth), [JWTCookie](../README.md#JWTCookie), [JWT](../README.md#JWT)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | ... retrieved successfully |  -  |
**400** | Bad request, Test  id number needs to be present! |  -  |
**500** | Internal server error |  -  |
**404** | Data not found |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_boms_for_series**
> BomDto get_boms_for_series(series_id)

Retrieve a bom by its Test series id

### Example

* Api Key Authentication (APIKeyV1):
* Api Key Authentication (CredentialsParameter):
* Basic Authentication (BasicAuth):
* Api Key Authentication (JWTCookie):
* Bearer (JWT) Authentication (JWT):

```python
import gbs3api
from gbs3api.models.bom_dto import BomDto
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
    api_instance = gbs3api.ReportDataSourcesApi(api_client)
    series_id = 56 # int | The ID of the series

    try:
        # Retrieve a bom by its Test series id
        api_response = api_instance.get_boms_for_series(series_id)
        print("The response of ReportDataSourcesApi->get_boms_for_series:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling ReportDataSourcesApi->get_boms_for_series: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **series_id** | **int**| The ID of the series | 

### Return type

[**BomDto**](BomDto.md)

### Authorization

[APIKeyV1](../README.md#APIKeyV1), [CredentialsParameter](../README.md#CredentialsParameter), [BasicAuth](../README.md#BasicAuth), [JWTCookie](../README.md#JWTCookie), [JWT](../README.md#JWT)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Bom retrieved successfully |  -  |
**400** | Bad request, Series id number needs to be present! |  -  |
**404** | Series Id or Bom not found |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_boms_for_test**
> BomDto get_boms_for_test(test_id)

Retrieve a Bom by its testId 

### Example

* Api Key Authentication (APIKeyV1):
* Api Key Authentication (CredentialsParameter):
* Basic Authentication (BasicAuth):
* Api Key Authentication (JWTCookie):
* Bearer (JWT) Authentication (JWT):

```python
import gbs3api
from gbs3api.models.bom_dto import BomDto
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
    api_instance = gbs3api.ReportDataSourcesApi(api_client)
    test_id = 56 # int | The ID of the one TestStep

    try:
        # Retrieve a Bom by its testId 
        api_response = api_instance.get_boms_for_test(test_id)
        print("The response of ReportDataSourcesApi->get_boms_for_test:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling ReportDataSourcesApi->get_boms_for_test: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **test_id** | **int**| The ID of the one TestStep | 

### Return type

[**BomDto**](BomDto.md)

### Authorization

[APIKeyV1](../README.md#APIKeyV1), [CredentialsParameter](../README.md#CredentialsParameter), [BasicAuth](../README.md#BasicAuth), [JWTCookie](../README.md#JWTCookie), [JWT](../README.md#JWT)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Bom retrieved successfully |  -  |
**400** | Bad request, Test id number needs to be present! |  -  |
**404** | Test ID not found |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_boms_for_test1**
> BomDto get_boms_for_test1(test_ids)

Retrieve a Bom by testIds

Returns Boms for given testIds. Example of emdpoint: http://localhost:8083/GBS/webservice/parts/boms/tests?testIds=86246337&testIds=86246692&testIds=86247047

### Example

* Api Key Authentication (APIKeyV1):
* Api Key Authentication (CredentialsParameter):
* Basic Authentication (BasicAuth):
* Api Key Authentication (JWTCookie):
* Bearer (JWT) Authentication (JWT):

```python
import gbs3api
from gbs3api.models.bom_dto import BomDto
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
    api_instance = gbs3api.ReportDataSourcesApi(api_client)
    test_ids = [86213995] # List[int] | Ids of tests

    try:
        # Retrieve a Bom by testIds
        api_response = api_instance.get_boms_for_test1(test_ids)
        print("The response of ReportDataSourcesApi->get_boms_for_test1:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling ReportDataSourcesApi->get_boms_for_test1: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **test_ids** | [**List[int]**](int.md)| Ids of tests | 

### Return type

[**BomDto**](BomDto.md)

### Authorization

[APIKeyV1](../README.md#APIKeyV1), [CredentialsParameter](../README.md#CredentialsParameter), [BasicAuth](../README.md#BasicAuth), [JWTCookie](../README.md#JWTCookie), [JWT](../README.md#JWT)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json, application/xml

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Bom retrieved successfully |  -  |
**400** | Bad request, Test id number needs to be present! |  -  |
**500** | Internal server error |  -  |
**404** | Test ID not found |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_component_test_groups**
> ComponentGroupDto get_component_test_groups(series_id, active_tests_only=active_tests_only)

Retrieve component group by its seriesId and active Tests

### Example

* Api Key Authentication (APIKeyV1):
* Api Key Authentication (CredentialsParameter):
* Basic Authentication (BasicAuth):
* Api Key Authentication (JWTCookie):
* Bearer (JWT) Authentication (JWT):

```python
import gbs3api
from gbs3api.models.component_group_dto import ComponentGroupDto
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
    api_instance = gbs3api.ReportDataSourcesApi(api_client)
    series_id = 56 # int | The ID of the series
    active_tests_only = True # bool |  (optional) (default to True)

    try:
        # Retrieve component group by its seriesId and active Tests
        api_response = api_instance.get_component_test_groups(series_id, active_tests_only=active_tests_only)
        print("The response of ReportDataSourcesApi->get_component_test_groups:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling ReportDataSourcesApi->get_component_test_groups: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **series_id** | **int**| The ID of the series | 
 **active_tests_only** | **bool**|  | [optional] [default to True]

### Return type

[**ComponentGroupDto**](ComponentGroupDto.md)

### Authorization

[APIKeyV1](../README.md#APIKeyV1), [CredentialsParameter](../README.md#CredentialsParameter), [BasicAuth](../README.md#BasicAuth), [JWTCookie](../README.md#JWTCookie), [JWT](../README.md#JWT)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Component group. retrieved successfully |  -  |
**400** | Bad request, Test series id number needs to be present! |  -  |
**404** | Series ID not found |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_devices_for_series**
> DeviceDto get_devices_for_series(series_id, vpnr_pos=vpnr_pos)

Retrieve a device by its seriesId and vpnrPos (TestStep position No.)

### Example

* Api Key Authentication (APIKeyV1):
* Api Key Authentication (CredentialsParameter):
* Basic Authentication (BasicAuth):
* Api Key Authentication (JWTCookie):
* Bearer (JWT) Authentication (JWT):

```python
import gbs3api
from gbs3api.models.device_dto import DeviceDto
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
    api_instance = gbs3api.ReportDataSourcesApi(api_client)
    series_id = 56 # int | The ID of the series
    vpnr_pos = [56] # List[int] | The TestStep position (No.) in Test Request (optional)

    try:
        # Retrieve a device by its seriesId and vpnrPos (TestStep position No.)
        api_response = api_instance.get_devices_for_series(series_id, vpnr_pos=vpnr_pos)
        print("The response of ReportDataSourcesApi->get_devices_for_series:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling ReportDataSourcesApi->get_devices_for_series: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **series_id** | **int**| The ID of the series | 
 **vpnr_pos** | [**List[int]**](int.md)| The TestStep position (No.) in Test Request | [optional] 

### Return type

[**DeviceDto**](DeviceDto.md)

### Authorization

[APIKeyV1](../README.md#APIKeyV1), [CredentialsParameter](../README.md#CredentialsParameter), [BasicAuth](../README.md#BasicAuth), [JWTCookie](../README.md#JWTCookie), [JWT](../README.md#JWT)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/xml, application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Device retrieved successfully |  -  |
**400** | Bad request, Test series id number needs to be present! |  -  |
**404** | Series ID or devices not found |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_devices_for_test**
> DeviceDto get_devices_for_test(test_id, vpnr_pos=vpnr_pos)

Retrieve a device by its TestStep Id and vpnrPos (TestStep position No.)

### Example

* Api Key Authentication (APIKeyV1):
* Api Key Authentication (CredentialsParameter):
* Basic Authentication (BasicAuth):
* Api Key Authentication (JWTCookie):
* Bearer (JWT) Authentication (JWT):

```python
import gbs3api
from gbs3api.models.device_dto import DeviceDto
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
    api_instance = gbs3api.ReportDataSourcesApi(api_client)
    test_id = 'test_id_example' # str | The ID of the TestStep(s). For multiple tests ID's enter using comma
    vpnr_pos = [56] # List[int] | The TestStep position (No.) in Test Request (optional)

    try:
        # Retrieve a device by its TestStep Id and vpnrPos (TestStep position No.)
        api_response = api_instance.get_devices_for_test(test_id, vpnr_pos=vpnr_pos)
        print("The response of ReportDataSourcesApi->get_devices_for_test:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling ReportDataSourcesApi->get_devices_for_test: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **test_id** | **str**| The ID of the TestStep(s). For multiple tests ID&#39;s enter using comma | 
 **vpnr_pos** | [**List[int]**](int.md)| The TestStep position (No.) in Test Request | [optional] 

### Return type

[**DeviceDto**](DeviceDto.md)

### Authorization

[APIKeyV1](../README.md#APIKeyV1), [CredentialsParameter](../README.md#CredentialsParameter), [BasicAuth](../README.md#BasicAuth), [JWTCookie](../README.md#JWTCookie), [JWT](../README.md#JWT)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Device retrieved successfully |  -  |
**400** | Bad request, TestStep id number needs to be present! |  -  |
**404** | TestStep Ids or devices not found |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_gbs_instance**
> GbsInstanceDto get_gbs_instance()

Retrieve GBS Instance

### Example

* Api Key Authentication (APIKeyV1):
* Api Key Authentication (CredentialsParameter):
* Basic Authentication (BasicAuth):
* Api Key Authentication (JWTCookie):
* Bearer (JWT) Authentication (JWT):

```python
import gbs3api
from gbs3api.models.gbs_instance_dto import GbsInstanceDto
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
    api_instance = gbs3api.ReportDataSourcesApi(api_client)

    try:
        # Retrieve GBS Instance
        api_response = api_instance.get_gbs_instance()
        print("The response of ReportDataSourcesApi->get_gbs_instance:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling ReportDataSourcesApi->get_gbs_instance: %s\n" % e)
```



### Parameters

This endpoint does not need any parameter.

### Return type

[**GbsInstanceDto**](GbsInstanceDto.md)

### Authorization

[APIKeyV1](../README.md#APIKeyV1), [CredentialsParameter](../README.md#CredentialsParameter), [BasicAuth](../README.md#BasicAuth), [JWTCookie](../README.md#JWTCookie), [JWT](../README.md#JWT)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | GBS Instance retrieved successfully |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_get_component_matrix_test_steps**
> MatrixStepDto get_get_component_matrix_test_steps(series_id, active_tests_only=active_tests_only, wrap_to_one_node=wrap_to_one_node)

Retrieve Matrix TestSteps by its seriesId and active tests only and wrap to one node

### Example

* Api Key Authentication (APIKeyV1):
* Api Key Authentication (CredentialsParameter):
* Basic Authentication (BasicAuth):
* Api Key Authentication (JWTCookie):
* Bearer (JWT) Authentication (JWT):

```python
import gbs3api
from gbs3api.models.matrix_step_dto import MatrixStepDto
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
    api_instance = gbs3api.ReportDataSourcesApi(api_client)
    series_id = 56 # int | The ID of the series
    active_tests_only = True # bool |  (optional) (default to True)
    wrap_to_one_node = True # bool |  (optional) (default to True)

    try:
        # Retrieve Matrix TestSteps by its seriesId and active tests only and wrap to one node
        api_response = api_instance.get_get_component_matrix_test_steps(series_id, active_tests_only=active_tests_only, wrap_to_one_node=wrap_to_one_node)
        print("The response of ReportDataSourcesApi->get_get_component_matrix_test_steps:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling ReportDataSourcesApi->get_get_component_matrix_test_steps: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **series_id** | **int**| The ID of the series | 
 **active_tests_only** | **bool**|  | [optional] [default to True]
 **wrap_to_one_node** | **bool**|  | [optional] [default to True]

### Return type

[**MatrixStepDto**](MatrixStepDto.md)

### Authorization

[APIKeyV1](../README.md#APIKeyV1), [CredentialsParameter](../README.md#CredentialsParameter), [BasicAuth](../README.md#BasicAuth), [JWTCookie](../README.md#JWTCookie), [JWT](../README.md#JWT)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Matrix TestSteps retrieved successfully |  -  |
**400** | Bad request, Test series id number needs to be present! |  -  |
**404** | Series ID not found |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_parts_for_series**
> PartDto get_parts_for_series(series_id)

Retrieve parts by its seriesId

### Example

* Api Key Authentication (APIKeyV1):
* Api Key Authentication (CredentialsParameter):
* Basic Authentication (BasicAuth):
* Api Key Authentication (JWTCookie):
* Bearer (JWT) Authentication (JWT):

```python
import gbs3api
from gbs3api.models.part_dto import PartDto
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
    api_instance = gbs3api.ReportDataSourcesApi(api_client)
    series_id = 56 # int | The ID of the series

    try:
        # Retrieve parts by its seriesId
        api_response = api_instance.get_parts_for_series(series_id)
        print("The response of ReportDataSourcesApi->get_parts_for_series:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling ReportDataSourcesApi->get_parts_for_series: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **series_id** | **int**| The ID of the series | 

### Return type

[**PartDto**](PartDto.md)

### Authorization

[APIKeyV1](../README.md#APIKeyV1), [CredentialsParameter](../README.md#CredentialsParameter), [BasicAuth](../README.md#BasicAuth), [JWTCookie](../README.md#JWTCookie), [JWT](../README.md#JWT)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json, application/xml

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Parts retrieved successfully |  -  |
**400** | Bad request, Test series id number needs to be present! |  -  |
**404** | Series ID not found |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_parts_for_test**
> PartDto get_parts_for_test(test_id)

Retrieve parts by its test Id

### Example

* Api Key Authentication (APIKeyV1):
* Api Key Authentication (CredentialsParameter):
* Basic Authentication (BasicAuth):
* Api Key Authentication (JWTCookie):
* Bearer (JWT) Authentication (JWT):

```python
import gbs3api
from gbs3api.models.part_dto import PartDto
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
    api_instance = gbs3api.ReportDataSourcesApi(api_client)
    test_id = 56 # int | The ID of the one TestStep

    try:
        # Retrieve parts by its test Id
        api_response = api_instance.get_parts_for_test(test_id)
        print("The response of ReportDataSourcesApi->get_parts_for_test:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling ReportDataSourcesApi->get_parts_for_test: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **test_id** | **int**| The ID of the one TestStep | 

### Return type

[**PartDto**](PartDto.md)

### Authorization

[APIKeyV1](../README.md#APIKeyV1), [CredentialsParameter](../README.md#CredentialsParameter), [BasicAuth](../README.md#BasicAuth), [JWTCookie](../README.md#JWTCookie), [JWT](../README.md#JWT)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Parts retrieved successfully |  -  |
**400** | Bad request, Test id number needs to be present! |  -  |
**404** | Test ID not found |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_parts_for_tests**
> PartDto get_parts_for_tests(test_ids)

Retrieve parts by test Ids

Return parts for test Ids. Example of endpoint: http://localhost:8083/GBS/webservice/parts/tests?testIds=86215369&testIds=86214852&testIds=86213995 

### Example

* Api Key Authentication (APIKeyV1):
* Api Key Authentication (CredentialsParameter):
* Basic Authentication (BasicAuth):
* Api Key Authentication (JWTCookie):
* Bearer (JWT) Authentication (JWT):

```python
import gbs3api
from gbs3api.models.part_dto import PartDto
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
    api_instance = gbs3api.ReportDataSourcesApi(api_client)
    test_ids = [86213995] # List[int] | Ids of tests

    try:
        # Retrieve parts by test Ids
        api_response = api_instance.get_parts_for_tests(test_ids)
        print("The response of ReportDataSourcesApi->get_parts_for_tests:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling ReportDataSourcesApi->get_parts_for_tests: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **test_ids** | [**List[int]**](int.md)| Ids of tests | 

### Return type

[**PartDto**](PartDto.md)

### Authorization

[APIKeyV1](../README.md#APIKeyV1), [CredentialsParameter](../README.md#CredentialsParameter), [BasicAuth](../README.md#BasicAuth), [JWTCookie](../README.md#JWTCookie), [JWT](../README.md#JWT)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json, application/xml

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Parts retrieved successfully |  -  |
**400** | Bad request, Test id number needs to be present! |  -  |
**500** | Internal server error |  -  |
**404** | Test ID not found |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_test_series_summary**
> TestSeriesDto get_test_series_summary(series_id, test_ids=test_ids)

Retrieve General Information by its seriesId

### Example

* Api Key Authentication (APIKeyV1):
* Api Key Authentication (CredentialsParameter):
* Basic Authentication (BasicAuth):
* Api Key Authentication (JWTCookie):
* Bearer (JWT) Authentication (JWT):

```python
import gbs3api
from gbs3api.models.test_series_dto import TestSeriesDto
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
    api_instance = gbs3api.ReportDataSourcesApi(api_client)
    series_id = 56 # int | The ID of the series
    test_ids = [56] # List[int] |  (optional)

    try:
        # Retrieve General Information by its seriesId
        api_response = api_instance.get_test_series_summary(series_id, test_ids=test_ids)
        print("The response of ReportDataSourcesApi->get_test_series_summary:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling ReportDataSourcesApi->get_test_series_summary: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **series_id** | **int**| The ID of the series | 
 **test_ids** | [**List[int]**](int.md)|  | [optional] 

### Return type

[**TestSeriesDto**](TestSeriesDto.md)

### Authorization

[APIKeyV1](../README.md#APIKeyV1), [CredentialsParameter](../README.md#CredentialsParameter), [BasicAuth](../README.md#BasicAuth), [JWTCookie](../README.md#JWTCookie), [JWT](../README.md#JWT)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | General Information retrieved successfully |  -  |
**400** | Bad request, Test series id number needs to be present! |  -  |
**404** | Series ID not found |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_used_equipment_for_series**
> get_used_equipment_for_series(series_id, region=region, vpnr_pos=vpnr_pos)

Retrieve used equipment and devices by its seriesId and vpnrPos (TestStep position No.)

Returns all equipment and devices used in test serie. Example of endpoint: http://localhost:8083/GBS/webservice/equipment-devices/series/85102759?vpnrPos=1

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
    api_instance = gbs3api.ReportDataSourcesApi(api_client)
    series_id = 134235421 # int | Unique identifier of the Test Series (must be a numeric value)
    region = 'ENGLISH' # str | This is Region (optional)
    vpnr_pos = [1] # List[int] | This is in another words TestStep position No. Has to be >0 (optional)

    try:
        # Retrieve used equipment and devices by its seriesId and vpnrPos (TestStep position No.)
        api_instance.get_used_equipment_for_series(series_id, region=region, vpnr_pos=vpnr_pos)
    except Exception as e:
        print("Exception when calling ReportDataSourcesApi->get_used_equipment_for_series: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **series_id** | **int**| Unique identifier of the Test Series (must be a numeric value) | 
 **region** | **str**| This is Region | [optional] 
 **vpnr_pos** | [**List[int]**](int.md)| This is in another words TestStep position No. Has to be &gt;0 | [optional] 

### Return type

void (empty response body)

### Authorization

[APIKeyV1](../README.md#APIKeyV1), [CredentialsParameter](../README.md#CredentialsParameter), [BasicAuth](../README.md#BasicAuth), [JWTCookie](../README.md#JWTCookie), [JWT](../README.md#JWT)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json, application/xml

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Used equipment retrieved successfully |  -  |
**400** | Bad request, Test series id number needs to be present! |  -  |
**500** | Internal server error |  -  |
**404** | Series ID not found |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_used_equipment_for_series1**
> get_used_equipment_for_series1(series_id, vpnr_pos=vpnr_pos)

Retrieve used equipment by its seriesId and vpnrPos (TestStep position No.)

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
    api_instance = gbs3api.ReportDataSourcesApi(api_client)
    series_id = 56 # int | The ID of the series
    vpnr_pos = [56] # List[int] | The TestStep position (No.) in Test Request (optional)

    try:
        # Retrieve used equipment by its seriesId and vpnrPos (TestStep position No.)
        api_instance.get_used_equipment_for_series1(series_id, vpnr_pos=vpnr_pos)
    except Exception as e:
        print("Exception when calling ReportDataSourcesApi->get_used_equipment_for_series1: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **series_id** | **int**| The ID of the series | 
 **vpnr_pos** | [**List[int]**](int.md)| The TestStep position (No.) in Test Request | [optional] 

### Return type

void (empty response body)

### Authorization

[APIKeyV1](../README.md#APIKeyV1), [CredentialsParameter](../README.md#CredentialsParameter), [BasicAuth](../README.md#BasicAuth), [JWTCookie](../README.md#JWTCookie), [JWT](../README.md#JWT)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json, application/xml

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Used equipment retrieved successfully |  -  |
**400** | Bad request, Test series id number needs to be present! |  -  |
**404** | Series ID not found |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_used_equipment_for_test**
> TestStepDto get_used_equipment_for_test(test_id, wrap_to_one_node=wrap_to_one_node, vpnr_pos=vpnr_pos)

Retrieve used equipment by its seriesId and vpnrPos (TestStep position No.)

### Example

* Api Key Authentication (APIKeyV1):
* Api Key Authentication (CredentialsParameter):
* Basic Authentication (BasicAuth):
* Api Key Authentication (JWTCookie):
* Bearer (JWT) Authentication (JWT):

```python
import gbs3api
from gbs3api.models.test_step_dto import TestStepDto
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
    api_instance = gbs3api.ReportDataSourcesApi(api_client)
    test_id = 'test_id_example' # str | The ID of the TestStep(s). For multiple tests ID's enter using comma
    wrap_to_one_node = True # bool |  (optional) (default to True)
    vpnr_pos = [56] # List[int] |  (optional)

    try:
        # Retrieve used equipment by its seriesId and vpnrPos (TestStep position No.)
        api_response = api_instance.get_used_equipment_for_test(test_id, wrap_to_one_node=wrap_to_one_node, vpnr_pos=vpnr_pos)
        print("The response of ReportDataSourcesApi->get_used_equipment_for_test:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling ReportDataSourcesApi->get_used_equipment_for_test: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **test_id** | **str**| The ID of the TestStep(s). For multiple tests ID&#39;s enter using comma | 
 **wrap_to_one_node** | **bool**|  | [optional] [default to True]
 **vpnr_pos** | [**List[int]**](int.md)|  | [optional] 

### Return type

[**TestStepDto**](TestStepDto.md)

### Authorization

[APIKeyV1](../README.md#APIKeyV1), [CredentialsParameter](../README.md#CredentialsParameter), [BasicAuth](../README.md#BasicAuth), [JWTCookie](../README.md#JWTCookie), [JWT](../README.md#JWT)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Used equipment retrieved successfully |  -  |
**400** | Bad request, Test series id number needs to be present! |  -  |
**404** | Series ID or used equipment not found |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

