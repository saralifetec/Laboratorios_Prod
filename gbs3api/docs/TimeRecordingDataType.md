# TimeRecordingDataType


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**path** | **str** |  | [optional] 
**user** | **str** |  | 
**remark** | **str** |  | 
**task** | **str** |  | 
**hours** | **float** |  | [optional] 
**time_recording_date** | **datetime** |  | [optional] 
**element_name** | **str** |  | [optional] 

## Example

```python
from gbs3api.models.time_recording_data_type import TimeRecordingDataType

# TODO update the JSON string below
json = "{}"
# create an instance of TimeRecordingDataType from a JSON string
time_recording_data_type_instance = TimeRecordingDataType.from_json(json)
# print the JSON string representation of the object
print(TimeRecordingDataType.to_json())

# convert the object into a dict
time_recording_data_type_dict = time_recording_data_type_instance.to_dict()
# create an instance of TimeRecordingDataType from a dict
time_recording_data_type_from_dict = TimeRecordingDataType.from_dict(time_recording_data_type_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


