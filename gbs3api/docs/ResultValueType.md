# ResultValueType


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**path** | **str** |  | [optional] 
**value** | **float** |  | [optional] 
**unit** | **str** |  | 
**physical_dimension** | **str** |  | [optional] 
**calc_interval_begin** | **float** |  | [optional] 
**calc_interval_end** | **float** |  | [optional] 
**macro** | **str** |  | 
**errors_occurred** | **bool** |  | [optional] 
**name** | **str** |  | [optional] 
**element_name** | **str** |  | [optional] 

## Example

```python
from gbs3api.models.result_value_type import ResultValueType

# TODO update the JSON string below
json = "{}"
# create an instance of ResultValueType from a JSON string
result_value_type_instance = ResultValueType.from_json(json)
# print the JSON string representation of the object
print(ResultValueType.to_json())

# convert the object into a dict
result_value_type_dict = result_value_type_instance.to_dict()
# create an instance of ResultValueType from a dict
result_value_type_from_dict = ResultValueType.from_dict(result_value_type_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


