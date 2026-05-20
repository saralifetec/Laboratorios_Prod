# FilterMetadataAllowedValueDto


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**value** | **str** |  | [optional] 
**label** | **str** |  | [optional] 

## Example

```python
from gbs4api.models.filter_metadata_allowed_value_dto import FilterMetadataAllowedValueDto

# TODO update the JSON string below
json = "{}"
# create an instance of FilterMetadataAllowedValueDto from a JSON string
filter_metadata_allowed_value_dto_instance = FilterMetadataAllowedValueDto.from_json(json)
# print the JSON string representation of the object
print(FilterMetadataAllowedValueDto.to_json())

# convert the object into a dict
filter_metadata_allowed_value_dto_dict = filter_metadata_allowed_value_dto_instance.to_dict()
# create an instance of FilterMetadataAllowedValueDto from a dict
filter_metadata_allowed_value_dto_from_dict = FilterMetadataAllowedValueDto.from_dict(filter_metadata_allowed_value_dto_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


