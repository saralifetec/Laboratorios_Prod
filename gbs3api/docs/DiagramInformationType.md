# DiagramInformationType


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**path** | **str** |  | [optional] 
**source** | **str** |  | [optional] 
**additional_group** | [**List[AdditionalGroup]**](AdditionalGroup.md) |  | [optional] 
**element_name** | **str** |  | [optional] 

## Example

```python
from gbs3api.models.diagram_information_type import DiagramInformationType

# TODO update the JSON string below
json = "{}"
# create an instance of DiagramInformationType from a JSON string
diagram_information_type_instance = DiagramInformationType.from_json(json)
# print the JSON string representation of the object
print(DiagramInformationType.to_json())

# convert the object into a dict
diagram_information_type_dict = diagram_information_type_instance.to_dict()
# create an instance of DiagramInformationType from a dict
diagram_information_type_from_dict = DiagramInformationType.from_dict(diagram_information_type_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


