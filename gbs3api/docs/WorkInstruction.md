# WorkInstruction


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**path** | **str** |  | [optional] 
**name** | **str** |  | 
**version** | **str** |  | 
**remote_link** | **str** |  | [optional] 
**additional_group** | [**List[AdditionalGroup]**](AdditionalGroup.md) |  | [optional] 
**element_name** | **str** |  | [optional] 

## Example

```python
from gbs3api.models.work_instruction import WorkInstruction

# TODO update the JSON string below
json = "{}"
# create an instance of WorkInstruction from a JSON string
work_instruction_instance = WorkInstruction.from_json(json)
# print the JSON string representation of the object
print(WorkInstruction.to_json())

# convert the object into a dict
work_instruction_dict = work_instruction_instance.to_dict()
# create an instance of WorkInstruction from a dict
work_instruction_from_dict = WorkInstruction.from_dict(work_instruction_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


