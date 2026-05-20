# ResultTypeType


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**path** | **str** |  | [optional] 
**value** | [**List[ResultValueType]**](ResultValueType.md) |  | 
**type** | **str** |  | [optional] 
**source** | **str** |  | [optional] 
**element_name** | **str** |  | [optional] 

## Example

```python
from gbs3api.models.result_type_type import ResultTypeType

# TODO update the JSON string below
json = "{}"
# create an instance of ResultTypeType from a JSON string
result_type_type_instance = ResultTypeType.from_json(json)
# print the JSON string representation of the object
print(ResultTypeType.to_json())

# convert the object into a dict
result_type_type_dict = result_type_type_instance.to_dict()
# create an instance of ResultTypeType from a dict
result_type_type_from_dict = ResultTypeType.from_dict(result_type_type_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


