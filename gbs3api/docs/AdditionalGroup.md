# AdditionalGroup


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**path** | **str** |  | [optional] 
**additional** | [**List[AdditionalAttributeType]**](AdditionalAttributeType.md) |  | 
**payload** | [**Payload**](Payload.md) |  | [optional] 
**sub_additional_group** | [**List[AdditionalGroup]**](AdditionalGroup.md) |  | [optional] 
**name** | **str** |  | [optional] 
**type** | **str** |  | [optional] 
**category** | **str** |  | [optional] 
**description** | **str** |  | [optional] 
**sort_index** | **int** |  | [optional] 
**is_available** | **str** |  | [optional] 
**element_name** | **str** |  | [optional] 

## Example

```python
from gbs3api.models.additional_group import AdditionalGroup

# TODO update the JSON string below
json = "{}"
# create an instance of AdditionalGroup from a JSON string
additional_group_instance = AdditionalGroup.from_json(json)
# print the JSON string representation of the object
print(AdditionalGroup.to_json())

# convert the object into a dict
additional_group_dict = additional_group_instance.to_dict()
# create an instance of AdditionalGroup from a dict
additional_group_from_dict = AdditionalGroup.from_dict(additional_group_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


