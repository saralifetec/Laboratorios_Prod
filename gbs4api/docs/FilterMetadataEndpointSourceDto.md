# FilterMetadataEndpointSourceDto


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**method** | **str** |  | [optional] 
**url** | **str** |  | [optional] 
**value_field** | **str** |  | [optional] 
**label_field** | **str** |  | [optional] 
**label_template** | **str** |  | [optional] 

## Example

```python
from gbs4api.models.filter_metadata_endpoint_source_dto import FilterMetadataEndpointSourceDto

# TODO update the JSON string below
json = "{}"
# create an instance of FilterMetadataEndpointSourceDto from a JSON string
filter_metadata_endpoint_source_dto_instance = FilterMetadataEndpointSourceDto.from_json(json)
# print the JSON string representation of the object
print(FilterMetadataEndpointSourceDto.to_json())

# convert the object into a dict
filter_metadata_endpoint_source_dto_dict = filter_metadata_endpoint_source_dto_instance.to_dict()
# create an instance of FilterMetadataEndpointSourceDto from a dict
filter_metadata_endpoint_source_dto_from_dict = FilterMetadataEndpointSourceDto.from_dict(filter_metadata_endpoint_source_dto_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


