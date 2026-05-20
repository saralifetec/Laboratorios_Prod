# ComponentTestGroupType


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**path** | **str** |  | [optional] 
**name** | **str** |  | 
**description** | **str** |  | [optional] 
**position** | **int** |  | [optional] 
**element_name** | **str** |  | [optional] 

## Example

```python
from gbs3api.models.component_test_group_type import ComponentTestGroupType

# TODO update the JSON string below
json = "{}"
# create an instance of ComponentTestGroupType from a JSON string
component_test_group_type_instance = ComponentTestGroupType.from_json(json)
# print the JSON string representation of the object
print(ComponentTestGroupType.to_json())

# convert the object into a dict
component_test_group_type_dict = component_test_group_type_instance.to_dict()
# create an instance of ComponentTestGroupType from a dict
component_test_group_type_from_dict = ComponentTestGroupType.from_dict(component_test_group_type_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


