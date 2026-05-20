# TestObjectType


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**path** | **str** |  | [optional] 
**name_of_test_object** | **str** |  | 
**velocity_test_object** | **str** |  | 
**mass_test_object** | **str** |  | 
**driver_position_object** | **str** |  | [optional] 
**impact_side_test_object** | **str** |  | 
**type_of_test_object** | **str** |  | 
**class_of_test_object** | **str** |  | [optional] 
**code_of_test_object** | **str** |  | [optional] 
**ref_number_of_test_object** | **str** |  | [optional] 
**seat_position** | [**List[SeatPositionType]**](SeatPositionType.md) |  | [optional] 
**additional_group** | [**List[AdditionalGroup]**](AdditionalGroup.md) |  | [optional] 
**element_name** | **str** |  | [optional] 

## Example

```python
from gbs3api.models.test_object_type import TestObjectType

# TODO update the JSON string below
json = "{}"
# create an instance of TestObjectType from a JSON string
test_object_type_instance = TestObjectType.from_json(json)
# print the JSON string representation of the object
print(TestObjectType.to_json())

# convert the object into a dict
test_object_type_dict = test_object_type_instance.to_dict()
# create an instance of TestObjectType from a dict
test_object_type_from_dict = TestObjectType.from_dict(test_object_type_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


