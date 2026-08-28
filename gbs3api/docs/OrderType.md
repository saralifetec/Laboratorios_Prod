# OrderType


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**path** | **str** |  | [optional] 
**netplan** | **str** |  | 
**platform** | **str** |  | [optional] 
**lab_netplans** | **str** |  | [optional] 
**creator** | **str** |  | [optional] 
**creation_date** | **datetime** |  | [optional] 
**start_date** | **datetime** |  | [optional] 
**target_lab_date** | **datetime** |  | [optional] 
**target_date_sample** | **datetime** |  | [optional] 
**location** | **str** |  | [optional] 
**real_finish_date** | **datetime** |  | [optional] 
**sample_type** | **str** |  | [optional] 
**build_purpose** | **str** |  | [optional] 
**sample** | [**List[SampleDataType]**](SampleDataType.md) |  | [optional] 
**additional_group** | [**List[AdditionalGroup]**](AdditionalGroup.md) |  | [optional] 
**pspelement** | **str** |  | [optional] 
**pbsid** | **str** |  | [optional] 
**element_name** | **str** |  | [optional] 

## Example

```python
from gbs3api.models.order_type import OrderType

# TODO update the JSON string below
json = "{}"
# create an instance of OrderType from a JSON string
order_type_instance = OrderType.from_json(json)
# print the JSON string representation of the object
print(OrderType.to_json())

# convert the object into a dict
order_type_dict = order_type_instance.to_dict()
# create an instance of OrderType from a dict
order_type_from_dict = OrderType.from_dict(order_type_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


