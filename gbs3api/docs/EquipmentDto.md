# EquipmentDto


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**level** | **str** |  | [optional] 
**equipment_id** | **int** |  | [optional] 
**resource_name** | **str** |  | [optional] 
**equipment_name** | **str** |  | [optional] 
**manufacturer** | **str** |  | [optional] 
**model** | **str** |  | [optional] 
**serial_number** | **str** |  | [optional] 
**ident_number** | **str** |  | [optional] 
**status** | **str** |  | [optional] 
**calibration_date** | **str** |  | [optional] 
**next_calibration_date** | **str** |  | [optional] 

## Example

```python
from gbs3api.models.equipment_dto import EquipmentDto

# TODO update the JSON string below
json = "{}"
# create an instance of EquipmentDto from a JSON string
equipment_dto_instance = EquipmentDto.from_json(json)
# print the JSON string representation of the object
print(EquipmentDto.to_json())

# convert the object into a dict
equipment_dto_dict = equipment_dto_instance.to_dict()
# create an instance of EquipmentDto from a dict
equipment_dto_from_dict = EquipmentDto.from_dict(equipment_dto_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


