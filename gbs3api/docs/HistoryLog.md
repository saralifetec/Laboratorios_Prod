# HistoryLog


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**id** | **int** |  | 
**user_id** | **str** |  | 
**date_of_change** | **datetime** |  | 
**entity_class** | **str** |  | 
**entity_id** | **str** |  | 
**action** | **str** |  | 
**history_log_entries** | [**List[HistoryLogEntry]**](HistoryLogEntry.md) |  | [optional] 

## Example

```python
from gbs3api.models.history_log import HistoryLog

# TODO update the JSON string below
json = "{}"
# create an instance of HistoryLog from a JSON string
history_log_instance = HistoryLog.from_json(json)
# print the JSON string representation of the object
print(HistoryLog.to_json())

# convert the object into a dict
history_log_dict = history_log_instance.to_dict()
# create an instance of HistoryLog from a dict
history_log_from_dict = HistoryLog.from_dict(history_log_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


