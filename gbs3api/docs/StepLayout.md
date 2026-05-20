# StepLayout


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**path** | **str** |  | [optional] 
**name** | **str** |  | 
**sort_index** | **int** |  | 
**jrxml_path** | **str** |  | 
**element_name** | **str** |  | [optional] 

## Example

```python
from gbs3api.models.step_layout import StepLayout

# TODO update the JSON string below
json = "{}"
# create an instance of StepLayout from a JSON string
step_layout_instance = StepLayout.from_json(json)
# print the JSON string representation of the object
print(StepLayout.to_json())

# convert the object into a dict
step_layout_dict = step_layout_instance.to_dict()
# create an instance of StepLayout from a dict
step_layout_from_dict = StepLayout.from_dict(step_layout_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


