# SampleTypeDataType


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**path** | **str** |  | [optional] 
**number** | **str** |  | 
**design_drawing_number** | **str** |  | [optional] 
**additional_group** | [**List[AdditionalGroup]**](AdditionalGroup.md) |  | [optional] 
**element_name** | **str** |  | [optional] 

## Example

```python
from gbs3api.models.sample_type_data_type import SampleTypeDataType

# TODO update the JSON string below
json = "{}"
# create an instance of SampleTypeDataType from a JSON string
sample_type_data_type_instance = SampleTypeDataType.from_json(json)
# print the JSON string representation of the object
print(SampleTypeDataType.to_json())

# convert the object into a dict
sample_type_data_type_dict = sample_type_data_type_instance.to_dict()
# create an instance of SampleTypeDataType from a dict
sample_type_data_type_from_dict = SampleTypeDataType.from_dict(sample_type_data_type_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


