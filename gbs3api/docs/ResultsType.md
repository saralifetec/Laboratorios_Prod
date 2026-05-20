# ResultsType


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**path** | **str** |  | [optional] 
**result** | [**List[ResultTypeType]**](ResultTypeType.md) |  | 
**element_name** | **str** |  | [optional] 

## Example

```python
from gbs3api.models.results_type import ResultsType

# TODO update the JSON string below
json = "{}"
# create an instance of ResultsType from a JSON string
results_type_instance = ResultsType.from_json(json)
# print the JSON string representation of the object
print(ResultsType.to_json())

# convert the object into a dict
results_type_dict = results_type_instance.to_dict()
# create an instance of ResultsType from a dict
results_type_from_dict = ResultsType.from_dict(results_type_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


