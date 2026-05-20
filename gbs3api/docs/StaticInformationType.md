# StaticInformationType


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**path** | **str** |  | [optional] 
**source** | **str** |  | [optional] 
**additional_group** | [**List[AdditionalGroup]**](AdditionalGroup.md) |  | [optional] 
**element_name** | **str** |  | [optional] 

## Example

```python
from gbs3api.models.static_information_type import StaticInformationType

# TODO update the JSON string below
json = "{}"
# create an instance of StaticInformationType from a JSON string
static_information_type_instance = StaticInformationType.from_json(json)
# print the JSON string representation of the object
print(StaticInformationType.to_json())

# convert the object into a dict
static_information_type_dict = static_information_type_instance.to_dict()
# create an instance of StaticInformationType from a dict
static_information_type_from_dict = StaticInformationType.from_dict(static_information_type_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


