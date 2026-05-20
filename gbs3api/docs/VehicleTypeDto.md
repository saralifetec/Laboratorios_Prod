# VehicleTypeDto


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**id** | **int** |  | [optional] 
**platform_code** | **str** |  | [optional] 
**market_code** | **str** |  | [optional] 
**producer** | **str** |  | [optional] 
**kba_category** | **str** |  | [optional] 

## Example

```python
from gbs3api.models.vehicle_type_dto import VehicleTypeDto

# TODO update the JSON string below
json = "{}"
# create an instance of VehicleTypeDto from a JSON string
vehicle_type_dto_instance = VehicleTypeDto.from_json(json)
# print the JSON string representation of the object
print(VehicleTypeDto.to_json())

# convert the object into a dict
vehicle_type_dto_dict = vehicle_type_dto_instance.to_dict()
# create an instance of VehicleTypeDto from a dict
vehicle_type_dto_from_dict = VehicleTypeDto.from_dict(vehicle_type_dto_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


