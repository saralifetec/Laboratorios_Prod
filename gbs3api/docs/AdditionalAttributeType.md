# AdditionalAttributeType


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**path** | **str** |  | [optional] 
**key** | **str** |  | [optional] 
**value** | **str** |  | [optional] 
**report_behaviour** | **str** |  | [optional] 
**additional_def_mandatory** | **str** |  | [optional] 
**data_type** | **str** |  | [optional] 
**category** | **str** |  | [optional] 
**file_path** | **str** |  | [optional] 
**element_name** | **str** |  | [optional] 

## Example

```python
from gbs3api.models.additional_attribute_type import AdditionalAttributeType

# TODO update the JSON string below
json = "{}"
# create an instance of AdditionalAttributeType from a JSON string
additional_attribute_type_instance = AdditionalAttributeType.from_json(json)
# print the JSON string representation of the object
print(AdditionalAttributeType.to_json())

# convert the object into a dict
additional_attribute_type_dict = additional_attribute_type_instance.to_dict()
# create an instance of AdditionalAttributeType from a dict
additional_attribute_type_from_dict = AdditionalAttributeType.from_dict(additional_attribute_type_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


