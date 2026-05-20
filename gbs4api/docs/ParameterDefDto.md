# ParameterDefDto


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**name** | **str** |  | 
**sort_index** | **int** |  | 
**value_list_name** | **str** |  | [optional] 
**test_facility_name** | **str** |  | 
**deprecated** | **bool** |  | [optional] 

## Example

```python
from gbs4api.models.parameter_def_dto import ParameterDefDto

# TODO update the JSON string below
json = "{}"
# create an instance of ParameterDefDto from a JSON string
parameter_def_dto_instance = ParameterDefDto.from_json(json)
# print the JSON string representation of the object
print(ParameterDefDto.to_json())

# convert the object into a dict
parameter_def_dto_dict = parameter_def_dto_instance.to_dict()
# create an instance of ParameterDefDto from a dict
parameter_def_dto_from_dict = ParameterDefDto.from_dict(parameter_def_dto_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


