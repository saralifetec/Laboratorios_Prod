# UUCGroup


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**path** | **str** |  | [optional] 
**found_in_test_series** | **str** |  | [optional] 
**name** | **str** |  | [optional] 
**model** | **str** |  | [optional] 
**serial_number** | **str** |  | [optional] 
**manufacturer** | **str** |  | [optional] 
**ident_nr** | **str** |  | [optional] 
**calibration_date** | **datetime** |  | [optional] 
**next_calibration_date** | **datetime** |  | [optional] 
**status** | **str** |  | [optional] 
**resource_name** | **str** |  | [optional] 
**element_name** | **str** |  | [optional] 

## Example

```python
from gbs3api.models.uuc_group import UUCGroup

# TODO update the JSON string below
json = "{}"
# create an instance of UUCGroup from a JSON string
uuc_group_instance = UUCGroup.from_json(json)
# print the JSON string representation of the object
print(UUCGroup.to_json())

# convert the object into a dict
uuc_group_dict = uuc_group_instance.to_dict()
# create an instance of UUCGroup from a dict
uuc_group_from_dict = UUCGroup.from_dict(uuc_group_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


