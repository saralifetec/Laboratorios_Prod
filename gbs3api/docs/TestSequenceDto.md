# TestSequenceDto


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**sequence_id** | **int** |  | [optional] 
**test_number** | **str** |  | [optional] 
**sort_index** | **int** |  | [optional] 
**vnumber** | **str** |  | [optional] 
**test_steps** | [**List[TestStepDto]**](TestStepDto.md) |  | [optional] 
**devices** | [**List[DeviceDto]**](DeviceDto.md) |  | [optional] 
**equipment** | [**List[EquipmentDto]**](EquipmentDto.md) |  | [optional] 
**additional_groups** | [**List[AdditionalGroupDto]**](AdditionalGroupDto.md) |  | [optional] 

## Example

```python
from gbs3api.models.test_sequence_dto import TestSequenceDto

# TODO update the JSON string below
json = "{}"
# create an instance of TestSequenceDto from a JSON string
test_sequence_dto_instance = TestSequenceDto.from_json(json)
# print the JSON string representation of the object
print(TestSequenceDto.to_json())

# convert the object into a dict
test_sequence_dto_dict = test_sequence_dto_instance.to_dict()
# create an instance of TestSequenceDto from a dict
test_sequence_dto_from_dict = TestSequenceDto.from_dict(test_sequence_dto_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


