# ScheduleDto


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**id** | **int** |  | [optional] 
**data_id** | **int** |  | [optional] 
**label** | **str** |  | [optional] 
**test_type** | **int** |  | 
**start_date** | **datetime** |  | [optional] 
**end_date** | **datetime** |  | [optional] 
**resources** | **List[int]** |  | [optional] 
**children** | **List[int]** |  | [optional] 
**parent** | **int** |  | [optional] 
**location** | **int** |  | [optional] 
**contact** | **int** |  | [optional] 
**requestor** | **int** |  | [optional] 
**info** | **str** |  | [optional] 
**color** | **str** |  | [optional] 
**status** | **str** |  | [optional] 
**part_count** | **int** |  | 
**version** | **int** |  | [optional] 
**history_comment** | **str** |  | [optional] 
**reason_for_change** | **str** |  | [optional] 
**event_type** | **str** |  | [optional] 
**is_background** | **bool** |  | [optional] 
**is_repeating** | **bool** |  | [optional] 
**is_forecast** | **bool** |  | [optional] 
**preceding** | **List[int]** |  | [optional] 
**subsequent** | **List[int]** |  | [optional] 
**active_parts** | **str** |  | [optional] [readonly] 

## Example

```python
from gbs3api.models.schedule_dto import ScheduleDto

# TODO update the JSON string below
json = "{}"
# create an instance of ScheduleDto from a JSON string
schedule_dto_instance = ScheduleDto.from_json(json)
# print the JSON string representation of the object
print(ScheduleDto.to_json())

# convert the object into a dict
schedule_dto_dict = schedule_dto_instance.to_dict()
# create an instance of ScheduleDto from a dict
schedule_dto_from_dict = ScheduleDto.from_dict(schedule_dto_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


