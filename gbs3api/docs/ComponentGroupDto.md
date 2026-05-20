# ComponentGroupDto


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**component_group_id** | **int** |  | [optional] 
**component_group_name** | **str** |  | [optional] 
**component_group_label** | **str** |  | [optional] 
**pos_index** | **int** |  | [optional] 
**part_count** | **int** |  | [optional] 
**sequences** | [**List[TestSequenceDto]**](TestSequenceDto.md) |  | [optional] 

## Example

```python
from gbs3api.models.component_group_dto import ComponentGroupDto

# TODO update the JSON string below
json = "{}"
# create an instance of ComponentGroupDto from a JSON string
component_group_dto_instance = ComponentGroupDto.from_json(json)
# print the JSON string representation of the object
print(ComponentGroupDto.to_json())

# convert the object into a dict
component_group_dto_dict = component_group_dto_instance.to_dict()
# create an instance of ComponentGroupDto from a dict
component_group_dto_from_dict = ComponentGroupDto.from_dict(component_group_dto_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


