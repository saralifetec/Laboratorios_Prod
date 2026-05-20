# DeviceDto


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**level** | **str** |  | [optional] 
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
from gbs3api.models.device_dto import DeviceDto

# TODO update the JSON string below
json = "{}"
# create an instance of DeviceDto from a JSON string
device_dto_instance = DeviceDto.from_json(json)
# print the JSON string representation of the object
print(DeviceDto.to_json())

# convert the object into a dict
device_dto_dict = device_dto_instance.to_dict()
# create an instance of DeviceDto from a dict
device_dto_from_dict = DeviceDto.from_dict(device_dto_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


