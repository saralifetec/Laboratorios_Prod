# FilterFieldMetadataDto


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**var_field** | **str** |  | [optional] 
**label** | **str** |  | [optional] 
**description** | **str** |  | [optional] 
**data_type** | **str** |  | [optional] 
**nullable** | **bool** |  | [optional] 
**constraints** | **Dict[str, object]** |  | [optional] 
**allowed_values** | [**FilterMetadataAllowedValuesDto**](FilterMetadataAllowedValuesDto.md) |  | [optional] 
**deprecated** | **bool** |  | [optional] 

## Example

```python
from gbs4api.models.filter_field_metadata_dto import FilterFieldMetadataDto

# TODO update the JSON string below
json = "{}"
# create an instance of FilterFieldMetadataDto from a JSON string
filter_field_metadata_dto_instance = FilterFieldMetadataDto.from_json(json)
# print the JSON string representation of the object
print(FilterFieldMetadataDto.to_json())

# convert the object into a dict
filter_field_metadata_dto_dict = filter_field_metadata_dto_instance.to_dict()
# create an instance of FilterFieldMetadataDto from a dict
filter_field_metadata_dto_from_dict = FilterFieldMetadataDto.from_dict(filter_field_metadata_dto_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


