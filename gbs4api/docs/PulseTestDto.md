# PulseTestDto


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**driver_position** | **int** |  | 
**customer_test_ref_no** | **str** |  | 
**laboratory_test_ref_no** | **str** |  | 
**date_of_test** | **date** |  | 
**status** | **str** |  | 
**impact_side** | **str** |  | [optional] 
**test_type** | **str** |  | [optional] 
**sub_test_type** | **str** |  | [optional] 
**proxy_person** | **str** |  | [optional] 
**person_in_charge** | **str** |  | 
**comment_ids** | **List[int]** |  | [optional] 
**channels** | **List[str]** |  | [optional] 
**external_test_id** | **str** |  | 
**pre_tests** | **List[str]** |  | [optional] 
**velocity** | **float** |  | [optional] 
**report_id** | **str** |  | [optional] 

## Example

```python
from gbs4api.models.pulse_test_dto import PulseTestDto

# TODO update the JSON string below
json = "{}"
# create an instance of PulseTestDto from a JSON string
pulse_test_dto_instance = PulseTestDto.from_json(json)
# print the JSON string representation of the object
print(PulseTestDto.to_json())

# convert the object into a dict
pulse_test_dto_dict = pulse_test_dto_instance.to_dict()
# create an instance of PulseTestDto from a dict
pulse_test_dto_from_dict = PulseTestDto.from_dict(pulse_test_dto_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


