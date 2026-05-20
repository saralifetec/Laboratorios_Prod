# RawInformationType


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**path** | **str** |  | [optional] 
**source** | **str** |  | [optional] 
**additional_group** | [**List[AdditionalGroup]**](AdditionalGroup.md) |  | [optional] 
**element_name** | **str** |  | [optional] 

## Example

```python
from gbs3api.models.raw_information_type import RawInformationType

# TODO update the JSON string below
json = "{}"
# create an instance of RawInformationType from a JSON string
raw_information_type_instance = RawInformationType.from_json(json)
# print the JSON string representation of the object
print(RawInformationType.to_json())

# convert the object into a dict
raw_information_type_dict = raw_information_type_instance.to_dict()
# create an instance of RawInformationType from a dict
raw_information_type_from_dict = RawInformationType.from_dict(raw_information_type_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


