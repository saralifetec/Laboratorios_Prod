# gbs4api.FilterMetadataControllerApi

All URIs are relative to *https://alfpwin0044.corp.passivesafety.com/gbs4-api*

Method | HTTP request | Description
------------- | ------------- | -------------
[**get_entity_metadata**](FilterMetadataControllerApi.md#get_entity_metadata) | **GET** /api/v1/filter-metadata/entities/{entityKey} | 
[**list_entities**](FilterMetadataControllerApi.md#list_entities) | **GET** /api/v1/filter-metadata/entities | 


# **get_entity_metadata**
> FilterEntityMetadataDto get_entity_metadata(entity_key)

### Example


```python
import gbs4api
from gbs4api.models.filter_entity_metadata_dto import FilterEntityMetadataDto
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
    api_instance = gbs4api.FilterMetadataControllerApi(api_client)
    entity_key = 'entity_key_example' # str | 

    try:
        api_response = api_instance.get_entity_metadata(entity_key)
        print("The response of FilterMetadataControllerApi->get_entity_metadata:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling FilterMetadataControllerApi->get_entity_metadata: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **entity_key** | **str**|  | 

### Return type

[**FilterEntityMetadataDto**](FilterEntityMetadataDto.md)

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

# **list_entities**
> List[FilterEntityDescriptorDto] list_entities()

### Example


```python
import gbs4api
from gbs4api.models.filter_entity_descriptor_dto import FilterEntityDescriptorDto
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
    api_instance = gbs4api.FilterMetadataControllerApi(api_client)

    try:
        api_response = api_instance.list_entities()
        print("The response of FilterMetadataControllerApi->list_entities:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling FilterMetadataControllerApi->list_entities: %s\n" % e)
```



### Parameters

This endpoint does not need any parameter.

### Return type

[**List[FilterEntityDescriptorDto]**](FilterEntityDescriptorDto.md)

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

