# PartsGroup


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**path** | **str** |  | [optional] 
**id** | **int** |  | [optional] 
**part_number** | **str** |  | [optional] 
**part_revision** | **str** |  | [optional] 
**customer_part_number** | **str** |  | [optional] 
**customer_part_revision** | **str** |  | [optional] 
**part_name** | **str** |  | [optional] 
**serial_number** | **str** |  | [optional] 
**production_date** | **datetime** |  | [optional] 
**manufacturer** | **str** |  | [optional] 
**description** | **str** |  | [optional] 
**inflator_serial_number** | **str** |  | [optional] 
**source_system_key** | **str** |  | [optional] 
**bom** | [**Bom**](Bom.md) |  | [optional] 
**element_name** | **str** |  | [optional] 

## Example

```python
from gbs3api.models.parts_group import PartsGroup

# TODO update the JSON string below
json = "{}"
# create an instance of PartsGroup from a JSON string
parts_group_instance = PartsGroup.from_json(json)
# print the JSON string representation of the object
print(PartsGroup.to_json())

# convert the object into a dict
parts_group_dict = parts_group_instance.to_dict()
# create an instance of PartsGroup from a dict
parts_group_from_dict = PartsGroup.from_dict(parts_group_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


