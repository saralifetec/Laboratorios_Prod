# HistoryLogEntry


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**id** | **int** |  | 
**var_property** | **str** |  | [optional] 
**previous_value** | **str** |  | [optional] 
**new_value** | **str** |  | [optional] 
**property_class** | **str** |  | [optional] 
**old_link_id** | **str** |  | [optional] 
**new_link_id** | **str** |  | [optional] 

## Example

```python
from gbs3api.models.history_log_entry import HistoryLogEntry

# TODO update the JSON string below
json = "{}"
# create an instance of HistoryLogEntry from a JSON string
history_log_entry_instance = HistoryLogEntry.from_json(json)
# print the JSON string representation of the object
print(HistoryLogEntry.to_json())

# convert the object into a dict
history_log_entry_dict = history_log_entry_instance.to_dict()
# create an instance of HistoryLogEntry from a dict
history_log_entry_from_dict = HistoryLogEntry.from_dict(history_log_entry_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


