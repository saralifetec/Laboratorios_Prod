# FilterMetadataAllowedValuesDto


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**mode** | **str** |  | [optional] 
**values** | [**List[FilterMetadataAllowedValueDto]**](FilterMetadataAllowedValueDto.md) |  | [optional] 
**endpoint** | [**FilterMetadataEndpointSourceDto**](FilterMetadataEndpointSourceDto.md) |  | [optional] 

## Example

```python
from gbs4api.models.filter_metadata_allowed_values_dto import FilterMetadataAllowedValuesDto

# TODO update the JSON string below
json = "{}"
# create an instance of FilterMetadataAllowedValuesDto from a JSON string
filter_metadata_allowed_values_dto_instance = FilterMetadataAllowedValuesDto.from_json(json)
# print the JSON string representation of the object
print(FilterMetadataAllowedValuesDto.to_json())

# convert the object into a dict
filter_metadata_allowed_values_dto_dict = filter_metadata_allowed_values_dto_instance.to_dict()
# create an instance of FilterMetadataAllowedValuesDto from a dict
filter_metadata_allowed_values_dto_from_dict = FilterMetadataAllowedValuesDto.from_dict(filter_metadata_allowed_values_dto_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


