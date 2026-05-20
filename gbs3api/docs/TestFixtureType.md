# TestFixtureType


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**path** | **str** |  | [optional] 
**name** | **str** |  | 
**category** | **str** |  | 
**resource_type_scheduling** | **str** |  | [optional] 
**resource_type_scheduling_id** | **str** |  | [optional] 
**additional_group** | [**List[AdditionalGroup]**](AdditionalGroup.md) |  | [optional] 
**element_name** | **str** |  | [optional] 

## Example

```python
from gbs3api.models.test_fixture_type import TestFixtureType

# TODO update the JSON string below
json = "{}"
# create an instance of TestFixtureType from a JSON string
test_fixture_type_instance = TestFixtureType.from_json(json)
# print the JSON string representation of the object
print(TestFixtureType.to_json())

# convert the object into a dict
test_fixture_type_dict = test_fixture_type_instance.to_dict()
# create an instance of TestFixtureType from a dict
test_fixture_type_from_dict = TestFixtureType.from_dict(test_fixture_type_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


