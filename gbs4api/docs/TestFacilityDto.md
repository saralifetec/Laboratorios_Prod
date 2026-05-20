# TestFacilityDto


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**name** | **str** |  | 
**remark** | **str** |  | [optional] 
**pre_tests_ids** | **List[int]** |  | [optional] 
**parameter_defs_ids** | **List[int]** |  | [optional] 
**persons** | **List[str]** |  | [optional] 
**location** | **int** |  | 

## Example

```python
from gbs4api.models.test_facility_dto import TestFacilityDto

# TODO update the JSON string below
json = "{}"
# create an instance of TestFacilityDto from a JSON string
test_facility_dto_instance = TestFacilityDto.from_json(json)
# print the JSON string representation of the object
print(TestFacilityDto.to_json())

# convert the object into a dict
test_facility_dto_dict = test_facility_dto_instance.to_dict()
# create an instance of TestFacilityDto from a dict
test_facility_dto_from_dict = TestFacilityDto.from_dict(test_facility_dto_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


