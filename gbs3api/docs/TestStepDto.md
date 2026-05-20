# TestStepDto


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**step_id** | **int** |  | [optional] 
**test_number** | **str** |  | [optional] 
**test_name** | **str** |  | [optional] 
**vpnr_pos** | **int** |  | [optional] 
**requestor_name** | **str** |  | [optional] 
**requestor_phone** | **str** |  | [optional] 
**subtype_of_test** | **str** |  | [optional] 
**devices** | [**List[DeviceDto]**](DeviceDto.md) |  | [optional] 
**equipment** | [**List[EquipmentDto]**](EquipmentDto.md) |  | [optional] 
**additional_groups** | [**List[AdditionalGroupDto]**](AdditionalGroupDto.md) |  | [optional] 

## Example

```python
from gbs3api.models.test_step_dto import TestStepDto

# TODO update the JSON string below
json = "{}"
# create an instance of TestStepDto from a JSON string
test_step_dto_instance = TestStepDto.from_json(json)
# print the JSON string representation of the object
print(TestStepDto.to_json())

# convert the object into a dict
test_step_dto_dict = test_step_dto_instance.to_dict()
# create an instance of TestStepDto from a dict
test_step_dto_from_dict = TestStepDto.from_dict(test_step_dto_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


