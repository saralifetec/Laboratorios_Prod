# TestFixtureStatusComment


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**path** | **str** |  | [optional] 
**comment_date** | **str** |  | 
**user** | **str** |  | 
**comment** | **str** |  | 
**old_status** | **str** |  | 
**new_status** | **str** |  | 
**element_name** | **str** |  | [optional] 

## Example

```python
from gbs3api.models.test_fixture_status_comment import TestFixtureStatusComment

# TODO update the JSON string below
json = "{}"
# create an instance of TestFixtureStatusComment from a JSON string
test_fixture_status_comment_instance = TestFixtureStatusComment.from_json(json)
# print the JSON string representation of the object
print(TestFixtureStatusComment.to_json())

# convert the object into a dict
test_fixture_status_comment_dict = test_fixture_status_comment_instance.to_dict()
# create an instance of TestFixtureStatusComment from a dict
test_fixture_status_comment_from_dict = TestFixtureStatusComment.from_dict(test_fixture_status_comment_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


