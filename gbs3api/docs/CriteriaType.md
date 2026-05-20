# CriteriaType


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**path** | **str** |  | [optional] 
**name** | **str** |  | 
**description** | **str** |  | [optional] 
**attribute_path** | **str** |  | [optional] 
**class_name** | **str** |  | [optional] 
**attribute** | **str** |  | [optional] 
**index** | **int** |  | 
**message** | **str** |  | 
**message_parameters** | **str** |  | [optional] 
**active** | **bool** |  | [optional] 
**element_name** | **str** |  | [optional] 

## Example

```python
from gbs3api.models.criteria_type import CriteriaType

# TODO update the JSON string below
json = "{}"
# create an instance of CriteriaType from a JSON string
criteria_type_instance = CriteriaType.from_json(json)
# print the JSON string representation of the object
print(CriteriaType.to_json())

# convert the object into a dict
criteria_type_dict = criteria_type_instance.to_dict()
# create an instance of CriteriaType from a dict
criteria_type_from_dict = CriteriaType.from_dict(criteria_type_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


