# FilterEntityDescriptorDto


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**key** | **str** |  | [optional] 
**label** | **str** |  | [optional] 
**description** | **str** |  | [optional] 
**endpoint** | **str** |  | [optional] 
**version** | **str** |  | [optional] 

## Example

```python
from gbs4api.models.filter_entity_descriptor_dto import FilterEntityDescriptorDto

# TODO update the JSON string below
json = "{}"
# create an instance of FilterEntityDescriptorDto from a JSON string
filter_entity_descriptor_dto_instance = FilterEntityDescriptorDto.from_json(json)
# print the JSON string representation of the object
print(FilterEntityDescriptorDto.to_json())

# convert the object into a dict
filter_entity_descriptor_dto_dict = filter_entity_descriptor_dto_instance.to_dict()
# create an instance of FilterEntityDescriptorDto from a dict
filter_entity_descriptor_dto_from_dict = FilterEntityDescriptorDto.from_dict(filter_entity_descriptor_dto_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


