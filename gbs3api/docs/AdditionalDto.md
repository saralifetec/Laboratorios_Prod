# AdditionalDto


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**additional_id** | **int** |  | [optional] 
**key** | **str** |  | [optional] 
**value** | **str** |  | [optional] 
**label** | **str** |  | [optional] 
**datatype** | **str** |  | [optional] 
**pos_index** | **int** |  | [optional] 
**file_path** | **str** |  | [optional] 
**additional_category** | **str** |  | [optional] 
**report_behaviour** | **str** |  | [optional] 
**print_behaviour** | **str** |  | [optional] 
**data_changed** | **str** |  | [optional] 

## Example

```python
from gbs3api.models.additional_dto import AdditionalDto

# TODO update the JSON string below
json = "{}"
# create an instance of AdditionalDto from a JSON string
additional_dto_instance = AdditionalDto.from_json(json)
# print the JSON string representation of the object
print(AdditionalDto.to_json())

# convert the object into a dict
additional_dto_dict = additional_dto_instance.to_dict()
# create an instance of AdditionalDto from a dict
additional_dto_from_dict = AdditionalDto.from_dict(additional_dto_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


