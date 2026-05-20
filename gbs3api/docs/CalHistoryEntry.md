# CalHistoryEntry


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**path** | **str** |  | [optional] 
**cal_version** | **int** |  | [optional] 
**scaling_method** | **str** |  | [optional] 
**sensitivity** | **float** |  | [optional] 
**engineering_unit** | **str** |  | [optional] 
**sensitivity2** | **float** |  | [optional] 
**sensitivity3** | **float** |  | [optional] 
**sensitivity4** | **float** |  | [optional] 
**sensitivity5** | **float** |  | [optional] 
**sensitivity_voltage** | **float** |  | [optional] 
**linearity_deviation** | **float** |  | [optional] 
**standard_deviation** | **float** |  | [optional] 
**cal_date** | **datetime** |  | [optional] 
**cal_person** | **str** |  | [optional] 
**cal_laboratory** | **str** |  | [optional] 
**cal_instruction** | **str** |  | [optional] 
**cal_remark** | **str** |  | [optional] 
**cal_protocol** | **str** |  | [optional] 
**reference_calibration** | **bool** |  | [optional] 
**hysteresis_deviation** | **float** |  | [optional] 
**additional_group** | [**List[AdditionalGroup]**](AdditionalGroup.md) |  | [optional] 
**element_name** | **str** |  | [optional] 

## Example

```python
from gbs3api.models.cal_history_entry import CalHistoryEntry

# TODO update the JSON string below
json = "{}"
# create an instance of CalHistoryEntry from a JSON string
cal_history_entry_instance = CalHistoryEntry.from_json(json)
# print the JSON string representation of the object
print(CalHistoryEntry.to_json())

# convert the object into a dict
cal_history_entry_dict = cal_history_entry_instance.to_dict()
# create an instance of CalHistoryEntry from a dict
cal_history_entry_from_dict = CalHistoryEntry.from_dict(cal_history_entry_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


