# ScheduleTypeDto


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**id** | **int** |  | [optional] 
**data_id** | **int** |  | [optional] 
**class_name** | **str** |  | [optional] 
**name** | **str** |  | [optional] 
**resource_types** | **List[int]** |  | [optional] 
**style_class** | **str** |  | [optional] 
**background** | **bool** |  | [optional] 

## Example

```python
from gbs3api.models.schedule_type_dto import ScheduleTypeDto

# TODO update the JSON string below
json = "{}"
# create an instance of ScheduleTypeDto from a JSON string
schedule_type_dto_instance = ScheduleTypeDto.from_json(json)
# print the JSON string representation of the object
print(ScheduleTypeDto.to_json())

# convert the object into a dict
schedule_type_dto_dict = schedule_type_dto_instance.to_dict()
# create an instance of ScheduleTypeDto from a dict
schedule_type_dto_from_dict = ScheduleTypeDto.from_dict(schedule_type_dto_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


