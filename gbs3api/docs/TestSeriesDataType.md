# TestSeriesDataType


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**path** | **str** |  | [optional] 
**number** | **str** |  | 
**remark** | **str** |  | [optional] 
**task** | **str** |  | [optional] 
**number_of_tests** | **int** |  | [optional] 
**estimated_start** | **datetime** |  | [optional] 
**estimated_end** | **datetime** |  | [optional] 
**actual_start** | **datetime** |  | [optional] 
**actual_end** | **datetime** |  | [optional] 
**order_date** | **datetime** |  | [optional] 
**creation_date** | **datetime** |  | [optional] 
**deadline_lab** | **datetime** |  | [optional] 
**series_start** | **datetime** |  | [optional] 
**lab_netplan** | **str** |  | [optional] 
**test_type** | **str** |  | [optional] 
**time_recordings** | [**List[TimeRecordingDataType]**](TimeRecordingDataType.md) |  | [optional] 
**feedback_talk** | [**FeedbackTalkDataType**](FeedbackTalkDataType.md) |  | [optional] 
**additional_group** | [**List[AdditionalGroup]**](AdditionalGroup.md) |  | [optional] 
**status** | **str** |  | [optional] 
**test_data** | [**List[TestDataType]**](TestDataType.md) |  | [optional] 
**order** | [**OrderType**](OrderType.md) |  | [optional] 
**vpn_r_pos** | [**List[VPnRPos]**](VPnRPos.md) |  | [optional] 
**element_name** | **str** |  | [optional] 
**sapnetplan** | **str** |  | [optional] 
**gdpimmilestone** | **str** |  | [optional] 

## Example

```python
from gbs3api.models.test_series_data_type import TestSeriesDataType

# TODO update the JSON string below
json = "{}"
# create an instance of TestSeriesDataType from a JSON string
test_series_data_type_instance = TestSeriesDataType.from_json(json)
# print the JSON string representation of the object
print(TestSeriesDataType.to_json())

# convert the object into a dict
test_series_data_type_dict = test_series_data_type_instance.to_dict()
# create an instance of TestSeriesDataType from a dict
test_series_data_type_from_dict = TestSeriesDataType.from_dict(test_series_data_type_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


