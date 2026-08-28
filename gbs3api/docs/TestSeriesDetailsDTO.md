# TestSeriesDetailsDTO


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**test_series_id** | **int** |  | [optional] 
**project_id** | **int** |  | [optional] 
**test_id** | **int** |  | [optional] 
**function_number** | **str** |  | [optional] 
**series_number** | **str** |  | [optional] 
**deadline_lab** | **datetime** |  | [optional] 
**estimated_start** | **datetime** |  | [optional] 
**estimated_end** | **datetime** |  | [optional] 
**series_start** | **datetime** |  | [optional] 
**actual_start** | **datetime** |  | [optional] 
**actual_end** | **datetime** |  | [optional] 
**order_date** | **datetime** |  | [optional] 
**creation_date** | **datetime** |  | [optional] 
**task** | **str** |  | [optional] 
**remark** | **str** |  | [optional] 
**lab_netplan** | **str** |  | [optional] 
**sap_netplan** | **str** |  | [optional] 
**status** | **str** |  | [optional] 
**wbs_element** | **str** |  | [optional] 
**customer_name** | **str** |  | [optional] 
**label** | **str** |  | [optional] 
**email** | **str** |  | [optional] 
**full_name** | **str** |  | [optional] 
**platform_code** | **str** |  | [optional] 
**development_phase** | **str** |  | [optional] 
**part_number** | **str** |  | [optional] 
**customer_part_number** | **str** |  | [optional] 

## Example

```python
from gbs3api.models.test_series_details_dto import TestSeriesDetailsDTO

# TODO update the JSON string below
json = "{}"
# create an instance of TestSeriesDetailsDTO from a JSON string
test_series_details_dto_instance = TestSeriesDetailsDTO.from_json(json)
# print the JSON string representation of the object
print(TestSeriesDetailsDTO.to_json())

# convert the object into a dict
test_series_details_dto_dict = test_series_details_dto_instance.to_dict()
# create an instance of TestSeriesDetailsDTO from a dict
test_series_details_dto_from_dict = TestSeriesDetailsDTO.from_dict(test_series_details_dto_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


