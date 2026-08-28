# TestStepDetailsDTO


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**test_series_id** | **int** |  | [optional] 
**schedule_parent** | **int** |  | [optional] 
**schedule_data_id** | **int** |  | [optional] 
**label** | **str** |  | [optional] 
**info** | **str** |  | [optional] 
**begin** | **datetime** |  | [optional] 
**end** | **datetime** |  | [optional] 
**part_count** | **int** |  | [optional] 
**sched_status** | **str** |  | [optional] 
**resource_name** | **str** |  | [optional] 
**class_name** | **str** |  | [optional] 
**resource_category** | **str** |  | [optional] 
**schedule_type** | **str** |  | [optional] 

## Example

```python
from gbs3api.models.test_step_details_dto import TestStepDetailsDTO

# TODO update the JSON string below
json = "{}"
# create an instance of TestStepDetailsDTO from a JSON string
test_step_details_dto_instance = TestStepDetailsDTO.from_json(json)
# print the JSON string representation of the object
print(TestStepDetailsDTO.to_json())

# convert the object into a dict
test_step_details_dto_dict = test_step_details_dto_instance.to_dict()
# create an instance of TestStepDetailsDTO from a dict
test_step_details_dto_from_dict = TestStepDetailsDTO.from_dict(test_step_details_dto_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


