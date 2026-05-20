# SensorGroup


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**path** | **str** |  | [optional] 
**category** | **str** |  | 
**name** | **str** |  | 
**uuid** | **str** |  | 
**sensor_group_status** | **str** |  | [optional] 
**serial_number** | **str** |  | [optional] 
**supplier** | **str** |  | [optional] 
**location** | **str** |  | [optional] 
**model** | **str** |  | [optional] 
**calibration_date** | **datetime** |  | [optional] 
**calibration_period** | **int** |  | [optional] 
**calibration_info** | **str** |  | [optional] 
**next_calibration_date** | **datetime** |  | [optional] 
**use_count** | **int** |  | [optional] 
**calibration_category** | **str** |  | [optional] 
**source_calibration** | [**CalHistoryEntry**](CalHistoryEntry.md) |  | [optional] 
**current_calibration** | [**CalHistoryEntry**](CalHistoryEntry.md) |  | [optional] 
**calibrations** | [**List[CalHistoryEntry]**](CalHistoryEntry.md) |  | [optional] 
**maintenance_category** | **str** |  | [optional] 
**maintenance_date** | **datetime** |  | [optional] 
**maintenance_period** | **int** |  | [optional] 
**next_maintenance_date** | **datetime** |  | [optional] 
**current_maintenance** | [**CalHistoryEntry**](CalHistoryEntry.md) |  | [optional] 
**maintenances** | [**List[CalHistoryEntry]**](CalHistoryEntry.md) |  | [optional] 
**verification_category** | **str** |  | [optional] 
**verification_date** | **datetime** |  | [optional] 
**verification_period** | **int** |  | [optional] 
**next_verification_date** | **datetime** |  | [optional] 
**current_verification** | [**CalHistoryEntry**](CalHistoryEntry.md) |  | [optional] 
**verifications** | [**List[CalHistoryEntry]**](CalHistoryEntry.md) |  | [optional] 
**resource_type_scheduling** | **str** |  | [optional] 
**resource_type_scheduling_id** | **str** |  | [optional] 
**sensor_groups** | [**List[SensorGroup]**](SensorGroup.md) |  | [optional] 
**sensor** | [**List[Sensor]**](Sensor.md) |  | 
**sensor_group_type** | [**SensorGroupType**](SensorGroupType.md) |  | [optional] 
**additional_group** | [**List[AdditionalGroup]**](AdditionalGroup.md) |  | [optional] 
**element_name** | **str** |  | [optional] 

## Example

```python
from gbs3api.models.sensor_group import SensorGroup

# TODO update the JSON string below
json = "{}"
# create an instance of SensorGroup from a JSON string
sensor_group_instance = SensorGroup.from_json(json)
# print the JSON string representation of the object
print(SensorGroup.to_json())

# convert the object into a dict
sensor_group_dict = sensor_group_instance.to_dict()
# create an instance of SensorGroup from a dict
sensor_group_from_dict = SensorGroup.from_dict(sensor_group_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


