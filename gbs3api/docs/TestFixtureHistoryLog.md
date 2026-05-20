# TestFixtureHistoryLog


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**path** | **str** |  | [optional] 
**comment_date** | **str** |  | 
**user** | **str** |  | 
**comment** | **str** |  | 
**element_name** | **str** |  | [optional] 

## Example

```python
from gbs3api.models.test_fixture_history_log import TestFixtureHistoryLog

# TODO update the JSON string below
json = "{}"
# create an instance of TestFixtureHistoryLog from a JSON string
test_fixture_history_log_instance = TestFixtureHistoryLog.from_json(json)
# print the JSON string representation of the object
print(TestFixtureHistoryLog.to_json())

# convert the object into a dict
test_fixture_history_log_dict = test_fixture_history_log_instance.to_dict()
# create an instance of TestFixtureHistoryLog from a dict
test_fixture_history_log_from_dict = TestFixtureHistoryLog.from_dict(test_fixture_history_log_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


