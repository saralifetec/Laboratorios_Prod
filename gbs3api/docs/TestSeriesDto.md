# TestSeriesDto


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**sequence_dtos** | [**List[TestSequenceDto]**](TestSequenceDto.md) |  | [optional] 
**series_id** | **int** |  | [optional] 
**series_number** | **str** |  | [optional] 
**development_phase** | **str** |  | [optional] 
**number_of_tests** | **int** |  | [optional] 
**estimated_start** | **datetime** |  | [optional] 
**estimated_end** | **datetime** |  | [optional] 
**actual_start** | **datetime** |  | [optional] 
**actual_end** | **datetime** |  | [optional] 
**parts_available** | **datetime** |  | [optional] 
**deadline_lab** | **datetime** |  | [optional] 
**creation_date** | **datetime** |  | [optional] 
**testtype** | **str** |  | [optional] 
**status** | **str** |  | [optional] 
**sap_netplan** | **str** |  | [optional] 
**lab_net_plan** | **str** |  | [optional] 
**remark** | **str** |  | [optional] 
**task** | **str** |  | [optional] 
**platform_code** | **str** |  | [optional] 
**market_code** | **str** |  | [optional] 
**producer** | **str** |  | [optional] 
**kba_category** | **str** |  | [optional] 
**tests_numbers_scope** | **str** |  | [optional] 
**first_part** | **str** |  | [optional] 
**last_part** | **str** |  | [optional] 
**customer_name** | **str** |  | [optional] 
**function_number** | **str** |  | [optional] 
**wbs_element** | **str** |  | [optional] 
**gbs_test_serie_link** | **str** |  | [optional] 
**responsible_location_address** | **str** |  | [optional] 
**project** | **str** |  | [optional] 
**sequences** | [**List[TestSequenceDto]**](TestSequenceDto.md) |  | [optional] 

## Example

```python
from gbs3api.models.test_series_dto import TestSeriesDto

# TODO update the JSON string below
json = "{}"
# create an instance of TestSeriesDto from a JSON string
test_series_dto_instance = TestSeriesDto.from_json(json)
# print the JSON string representation of the object
print(TestSeriesDto.to_json())

# convert the object into a dict
test_series_dto_dict = test_series_dto_instance.to_dict()
# create an instance of TestSeriesDto from a dict
test_series_dto_from_dict = TestSeriesDto.from_dict(test_series_dto_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


