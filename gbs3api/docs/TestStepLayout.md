# TestStepLayout


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**path** | **str** |  | [optional] 
**step_layout** | [**List[StepLayout]**](StepLayout.md) |  | 
**name** | **str** |  | 
**element_name** | **str** |  | [optional] 

## Example

```python
from gbs3api.models.test_step_layout import TestStepLayout

# TODO update the JSON string below
json = "{}"
# create an instance of TestStepLayout from a JSON string
test_step_layout_instance = TestStepLayout.from_json(json)
# print the JSON string representation of the object
print(TestStepLayout.to_json())

# convert the object into a dict
test_step_layout_dict = test_step_layout_instance.to_dict()
# create an instance of TestStepLayout from a dict
test_step_layout_from_dict = TestStepLayout.from_dict(test_step_layout_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


