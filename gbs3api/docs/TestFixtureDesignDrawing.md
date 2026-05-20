# TestFixtureDesignDrawing


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**path** | **str** |  | [optional] 
**name** | **str** |  | 
**description** | **str** |  | [optional] 
**index** | **str** |  | [optional] 
**link** | **str** |  | [optional] 
**additional_group** | [**List[AdditionalGroup]**](AdditionalGroup.md) |  | [optional] 
**element_name** | **str** |  | [optional] 

## Example

```python
from gbs3api.models.test_fixture_design_drawing import TestFixtureDesignDrawing

# TODO update the JSON string below
json = "{}"
# create an instance of TestFixtureDesignDrawing from a JSON string
test_fixture_design_drawing_instance = TestFixtureDesignDrawing.from_json(json)
# print the JSON string representation of the object
print(TestFixtureDesignDrawing.to_json())

# convert the object into a dict
test_fixture_design_drawing_dict = test_fixture_design_drawing_instance.to_dict()
# create an instance of TestFixtureDesignDrawing from a dict
test_fixture_design_drawing_from_dict = TestFixtureDesignDrawing.from_dict(test_fixture_design_drawing_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


