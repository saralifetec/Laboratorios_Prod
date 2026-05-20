# ExternalTestDto


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**driver_position** | **int** |  | 
**test_id** | **str** |  | 
**date_of_test** | **date** |  | 
**velocity_pulse** | **float** |  | 
**impact_side** | **str** |  | [optional] 
**test_type** | **str** |  | [optional] 
**sub_test_type** | **str** |  | [optional] 
**vehicle_type** | **str** |  | 
**proxy_person** | **str** |  | [optional] 
**person_in_charge** | **str** |  | 
**comment_ids** | **List[int]** |  | [optional] 
**channels** | **List[str]** |  | [optional] 
**pulses** | **List[str]** |  | [optional] 
**report_id** | **str** |  | [optional] 
**customer** | **str** |  | [optional] 

## Example

```python
from gbs4api.models.external_test_dto import ExternalTestDto

# TODO update the JSON string below
json = "{}"
# create an instance of ExternalTestDto from a JSON string
external_test_dto_instance = ExternalTestDto.from_json(json)
# print the JSON string representation of the object
print(ExternalTestDto.to_json())

# convert the object into a dict
external_test_dto_dict = external_test_dto_instance.to_dict()
# create an instance of ExternalTestDto from a dict
external_test_dto_from_dict = ExternalTestDto.from_dict(external_test_dto_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


