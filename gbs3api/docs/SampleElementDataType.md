# SampleElementDataType


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**path** | **str** |  | [optional] 
**number** | **str** |  | 
**description** | **str** |  | [optional] 
**type** | **str** |  | [optional] 
**additional_group** | [**AdditionalGroup**](AdditionalGroup.md) |  | [optional] 
**pbsbom_id** | **str** |  | [optional] 
**element_name** | **str** |  | [optional] 

## Example

```python
from gbs3api.models.sample_element_data_type import SampleElementDataType

# TODO update the JSON string below
json = "{}"
# create an instance of SampleElementDataType from a JSON string
sample_element_data_type_instance = SampleElementDataType.from_json(json)
# print the JSON string representation of the object
print(SampleElementDataType.to_json())

# convert the object into a dict
sample_element_data_type_dict = sample_element_data_type_instance.to_dict()
# create an instance of SampleElementDataType from a dict
sample_element_data_type_from_dict = SampleElementDataType.from_dict(sample_element_data_type_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


