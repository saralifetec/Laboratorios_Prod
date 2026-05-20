# gbs4api.ChannelControllerApi

All URIs are relative to *https://alfpwin0044.corp.passivesafety.com/gbs4-api*

Method | HTTP request | Description
------------- | ------------- | -------------
[**create_channel_for_external_test**](ChannelControllerApi.md#create_channel_for_external_test) | **POST** /api/v1/external-tests/{externalTestId}/channels | 
[**create_channel_for_pre_test**](ChannelControllerApi.md#create_channel_for_pre_test) | **POST** /api/v1/external-tests/{externalTestId}/pulses/{pulseTestCustomerRefNumber}/test-facilities/{testFacilityName}/pre-tests/{preTestCustomerRefNumber}/channels | 
[**create_channel_for_pulse_test**](ChannelControllerApi.md#create_channel_for_pulse_test) | **POST** /api/v1/external-tests/{externalTestId}/pulses/{pulseTestCustomerRefNumber}/channels | 
[**delete_channel_for_external_test**](ChannelControllerApi.md#delete_channel_for_external_test) | **DELETE** /api/v1/external-tests/{externalTestId}/channels/{channelId} | 
[**delete_channel_for_pre_test**](ChannelControllerApi.md#delete_channel_for_pre_test) | **DELETE** /api/v1/external-tests/{externalTestId}/pulses/{pulseTestCustomerRefNumber}/test-facilities/{testFacilityName}/pre-tests/{preTestCustomerRefNumber}/channels/{channelId} | 
[**delete_channel_for_pulse_test**](ChannelControllerApi.md#delete_channel_for_pulse_test) | **DELETE** /api/v1/external-tests/{externalTestId}/pulses/{pulseTestCustomerRefNumber}/channels/{channelId} | 
[**get_channels_for_external_test**](ChannelControllerApi.md#get_channels_for_external_test) | **GET** /api/v1/external-tests/{externalTestId}/channels | 
[**get_channels_for_pre_test**](ChannelControllerApi.md#get_channels_for_pre_test) | **GET** /api/v1/external-tests/{externalTestId}/pulses/{pulseTestCustomerRefNumber}/test-facilities/{testFacilityName}/pre-tests/{preTestCustomerRefNumber}/channels | 
[**get_channels_for_pulse_test**](ChannelControllerApi.md#get_channels_for_pulse_test) | **GET** /api/v1/external-tests/{externalTestId}/pulses/{pulseTestCustomerRefNumber}/channels | 


# **create_channel_for_external_test**
> create_channel_for_external_test(external_test_id, channel_dto)

### Example


```python
import gbs4api
from gbs4api.models.channel_dto import ChannelDto
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
    api_instance = gbs4api.ChannelControllerApi(api_client)
    external_test_id = 'external_test_id_example' # str | 
    channel_dto = gbs4api.ChannelDto() # ChannelDto | 

    try:
        api_instance.create_channel_for_external_test(external_test_id, channel_dto)
    except Exception as e:
        print("Exception when calling ChannelControllerApi->create_channel_for_external_test: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **external_test_id** | **str**|  | 
 **channel_dto** | [**ChannelDto**](ChannelDto.md)|  | 

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

# **create_channel_for_pre_test**
> create_channel_for_pre_test(external_test_id, pulse_test_customer_ref_number, test_facility_name, pre_test_customer_ref_number, channel_dto)

### Example


```python
import gbs4api
from gbs4api.models.channel_dto import ChannelDto
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
    api_instance = gbs4api.ChannelControllerApi(api_client)
    external_test_id = 'external_test_id_example' # str | 
    pulse_test_customer_ref_number = 'pulse_test_customer_ref_number_example' # str | 
    test_facility_name = 'test_facility_name_example' # str | 
    pre_test_customer_ref_number = 'pre_test_customer_ref_number_example' # str | 
    channel_dto = gbs4api.ChannelDto() # ChannelDto | 

    try:
        api_instance.create_channel_for_pre_test(external_test_id, pulse_test_customer_ref_number, test_facility_name, pre_test_customer_ref_number, channel_dto)
    except Exception as e:
        print("Exception when calling ChannelControllerApi->create_channel_for_pre_test: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **external_test_id** | **str**|  | 
 **pulse_test_customer_ref_number** | **str**|  | 
 **test_facility_name** | **str**|  | 
 **pre_test_customer_ref_number** | **str**|  | 
 **channel_dto** | [**ChannelDto**](ChannelDto.md)|  | 

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

# **create_channel_for_pulse_test**
> create_channel_for_pulse_test(external_test_id, pulse_test_customer_ref_number, channel_dto)

### Example


```python
import gbs4api
from gbs4api.models.channel_dto import ChannelDto
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
    api_instance = gbs4api.ChannelControllerApi(api_client)
    external_test_id = 'external_test_id_example' # str | 
    pulse_test_customer_ref_number = 'pulse_test_customer_ref_number_example' # str | 
    channel_dto = gbs4api.ChannelDto() # ChannelDto | 

    try:
        api_instance.create_channel_for_pulse_test(external_test_id, pulse_test_customer_ref_number, channel_dto)
    except Exception as e:
        print("Exception when calling ChannelControllerApi->create_channel_for_pulse_test: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **external_test_id** | **str**|  | 
 **pulse_test_customer_ref_number** | **str**|  | 
 **channel_dto** | [**ChannelDto**](ChannelDto.md)|  | 

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

# **delete_channel_for_external_test**
> delete_channel_for_external_test(external_test_id, channel_id)

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
    api_instance = gbs4api.ChannelControllerApi(api_client)
    external_test_id = 'external_test_id_example' # str | 
    channel_id = 56 # int | 

    try:
        api_instance.delete_channel_for_external_test(external_test_id, channel_id)
    except Exception as e:
        print("Exception when calling ChannelControllerApi->delete_channel_for_external_test: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **external_test_id** | **str**|  | 
 **channel_id** | **int**|  | 

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

# **delete_channel_for_pre_test**
> delete_channel_for_pre_test(external_test_id, pulse_test_customer_ref_number, test_facility_name, pre_test_customer_ref_number, channel_id)

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
    api_instance = gbs4api.ChannelControllerApi(api_client)
    external_test_id = 'external_test_id_example' # str | 
    pulse_test_customer_ref_number = 'pulse_test_customer_ref_number_example' # str | 
    test_facility_name = 'test_facility_name_example' # str | 
    pre_test_customer_ref_number = 'pre_test_customer_ref_number_example' # str | 
    channel_id = 56 # int | 

    try:
        api_instance.delete_channel_for_pre_test(external_test_id, pulse_test_customer_ref_number, test_facility_name, pre_test_customer_ref_number, channel_id)
    except Exception as e:
        print("Exception when calling ChannelControllerApi->delete_channel_for_pre_test: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **external_test_id** | **str**|  | 
 **pulse_test_customer_ref_number** | **str**|  | 
 **test_facility_name** | **str**|  | 
 **pre_test_customer_ref_number** | **str**|  | 
 **channel_id** | **int**|  | 

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

# **delete_channel_for_pulse_test**
> delete_channel_for_pulse_test(external_test_id, pulse_test_customer_ref_number, channel_id)

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
    api_instance = gbs4api.ChannelControllerApi(api_client)
    external_test_id = 'external_test_id_example' # str | 
    pulse_test_customer_ref_number = 'pulse_test_customer_ref_number_example' # str | 
    channel_id = 56 # int | 

    try:
        api_instance.delete_channel_for_pulse_test(external_test_id, pulse_test_customer_ref_number, channel_id)
    except Exception as e:
        print("Exception when calling ChannelControllerApi->delete_channel_for_pulse_test: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **external_test_id** | **str**|  | 
 **pulse_test_customer_ref_number** | **str**|  | 
 **channel_id** | **int**|  | 

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

# **get_channels_for_external_test**
> List[ChannelDto] get_channels_for_external_test(external_test_id)

### Example


```python
import gbs4api
from gbs4api.models.channel_dto import ChannelDto
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
    api_instance = gbs4api.ChannelControllerApi(api_client)
    external_test_id = 'external_test_id_example' # str | 

    try:
        api_response = api_instance.get_channels_for_external_test(external_test_id)
        print("The response of ChannelControllerApi->get_channels_for_external_test:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling ChannelControllerApi->get_channels_for_external_test: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **external_test_id** | **str**|  | 

### Return type

[**List[ChannelDto]**](ChannelDto.md)

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

# **get_channels_for_pre_test**
> List[ChannelDto] get_channels_for_pre_test(external_test_id, pulse_test_customer_ref_number, test_facility_name, pre_test_customer_ref_number)

### Example


```python
import gbs4api
from gbs4api.models.channel_dto import ChannelDto
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
    api_instance = gbs4api.ChannelControllerApi(api_client)
    external_test_id = 'external_test_id_example' # str | 
    pulse_test_customer_ref_number = 'pulse_test_customer_ref_number_example' # str | 
    test_facility_name = 'test_facility_name_example' # str | 
    pre_test_customer_ref_number = 'pre_test_customer_ref_number_example' # str | 

    try:
        api_response = api_instance.get_channels_for_pre_test(external_test_id, pulse_test_customer_ref_number, test_facility_name, pre_test_customer_ref_number)
        print("The response of ChannelControllerApi->get_channels_for_pre_test:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling ChannelControllerApi->get_channels_for_pre_test: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **external_test_id** | **str**|  | 
 **pulse_test_customer_ref_number** | **str**|  | 
 **test_facility_name** | **str**|  | 
 **pre_test_customer_ref_number** | **str**|  | 

### Return type

[**List[ChannelDto]**](ChannelDto.md)

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

# **get_channels_for_pulse_test**
> List[ChannelDto] get_channels_for_pulse_test(external_test_id, pulse_test_customer_ref_number)

### Example


```python
import gbs4api
from gbs4api.models.channel_dto import ChannelDto
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
    api_instance = gbs4api.ChannelControllerApi(api_client)
    external_test_id = 'external_test_id_example' # str | 
    pulse_test_customer_ref_number = 'pulse_test_customer_ref_number_example' # str | 

    try:
        api_response = api_instance.get_channels_for_pulse_test(external_test_id, pulse_test_customer_ref_number)
        print("The response of ChannelControllerApi->get_channels_for_pulse_test:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling ChannelControllerApi->get_channels_for_pulse_test: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **external_test_id** | **str**|  | 
 **pulse_test_customer_ref_number** | **str**|  | 

### Return type

[**List[ChannelDto]**](ChannelDto.md)

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

