# FilterEntityMetadataDto


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**key** | **str** |  | [optional] 
**label** | **str** |  | [optional] 
**description** | **str** |  | [optional] 
**endpoint** | **str** |  | [optional] 
**version** | **str** |  | [optional] 
**fields** | [**List[FilterFieldMetadataDto]**](FilterFieldMetadataDto.md) |  | [optional] 

## Example

```python
from gbs4api.models.filter_entity_metadata_dto import FilterEntityMetadataDto

# TODO update the JSON string below
json = "{}"
# create an instance of FilterEntityMetadataDto from a JSON string
filter_entity_metadata_dto_instance = FilterEntityMetadataDto.from_json(json)
# print the JSON string representation of the object
print(FilterEntityMetadataDto.to_json())

# convert the object into a dict
filter_entity_metadata_dto_dict = filter_entity_metadata_dto_instance.to_dict()
# create an instance of FilterEntityMetadataDto from a dict
filter_entity_metadata_dto_from_dict = FilterEntityMetadataDto.from_dict(filter_entity_metadata_dto_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


