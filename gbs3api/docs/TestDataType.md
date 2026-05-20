# TestDataType


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**path** | **str** |  | [optional] 
**instance** | **str** |  | [optional] 
**host** | **str** |  | [optional] 
**source** | **str** |  | [optional] 
**general_information** | [**GeneralInformationType**](GeneralInformationType.md) |  | 
**additional_group** | [**List[AdditionalGroup]**](AdditionalGroup.md) |  | [optional] 
**element_name** | **str** |  | [optional] 

## Example

```python
from gbs3api.models.test_data_type import TestDataType

# TODO update the JSON string below
json = "{}"
# create an instance of TestDataType from a JSON string
test_data_type_instance = TestDataType.from_json(json)
# print the JSON string representation of the object
print(TestDataType.to_json())

# convert the object into a dict
test_data_type_dict = test_data_type_instance.to_dict()
# create an instance of TestDataType from a dict
test_data_type_from_dict = TestDataType.from_dict(test_data_type_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


