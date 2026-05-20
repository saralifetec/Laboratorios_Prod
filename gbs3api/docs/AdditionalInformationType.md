# AdditionalInformationType


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**path** | **str** |  | [optional] 
**source** | **str** |  | [optional] 
**additional_group** | [**List[AdditionalGroup]**](AdditionalGroup.md) |  | [optional] 
**element_name** | **str** |  | [optional] 

## Example

```python
from gbs3api.models.additional_information_type import AdditionalInformationType

# TODO update the JSON string below
json = "{}"
# create an instance of AdditionalInformationType from a JSON string
additional_information_type_instance = AdditionalInformationType.from_json(json)
# print the JSON string representation of the object
print(AdditionalInformationType.to_json())

# convert the object into a dict
additional_information_type_dict = additional_information_type_instance.to_dict()
# create an instance of AdditionalInformationType from a dict
additional_information_type_from_dict = AdditionalInformationType.from_dict(additional_information_type_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


