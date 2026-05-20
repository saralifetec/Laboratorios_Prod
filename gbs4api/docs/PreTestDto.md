# PreTestDto


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**driver_position** | **int** |  | 
**customer_test_ref_no** | **str** |  | 
**laboratory_test_ref_no** | **str** |  | 
**date_of_test** | **date** |  | 
**velocity_pulse** | **float** |  | 
**pulse_status** | **str** |  | 
**impact_side** | **str** |  | [optional] 
**test_type** | **str** |  | [optional] 
**sub_test_type** | **str** |  | [optional] 
**proxy_person** | **str** |  | [optional] 
**person_in_charge** | **str** |  | 
**comment_ids** | **List[int]** |  | [optional] 
**channels** | **List[str]** |  | [optional] 
**pulse_test** | **str** |  | 
**test_facility** | **str** |  | 
**report_id** | **str** |  | [optional] 

## Example

```python
from gbs4api.models.pre_test_dto import PreTestDto

# TODO update the JSON string below
json = "{}"
# create an instance of PreTestDto from a JSON string
pre_test_dto_instance = PreTestDto.from_json(json)
# print the JSON string representation of the object
print(PreTestDto.to_json())

# convert the object into a dict
pre_test_dto_dict = pre_test_dto_instance.to_dict()
# create an instance of PreTestDto from a dict
pre_test_dto_from_dict = PreTestDto.from_dict(pre_test_dto_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


