# AdditionalGroupDto


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**group_id** | **int** |  | [optional] 
**name** | **str** |  | [optional] 
**label** | **str** |  | [optional] 
**category** | **str** |  | [optional] 
**sort_index** | **int** |  | [optional] 
**path** | **str** |  | [optional] 
**show_in_report** | **str** |  | [optional] 
**additionals** | [**List[AdditionalDto]**](AdditionalDto.md) |  | [optional] 
**child_groups** | [**List[AdditionalGroupDto]**](AdditionalGroupDto.md) |  | [optional] 

## Example

```python
from gbs3api.models.additional_group_dto import AdditionalGroupDto

# TODO update the JSON string below
json = "{}"
# create an instance of AdditionalGroupDto from a JSON string
additional_group_dto_instance = AdditionalGroupDto.from_json(json)
# print the JSON string representation of the object
print(AdditionalGroupDto.to_json())

# convert the object into a dict
additional_group_dto_dict = additional_group_dto_instance.to_dict()
# create an instance of AdditionalGroupDto from a dict
additional_group_dto_from_dict = AdditionalGroupDto.from_dict(additional_group_dto_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


