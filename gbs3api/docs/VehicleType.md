# VehicleType


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**path** | **str** |  | [optional] 
**platform_code** | **str** |  | 
**market_code** | **str** |  | 
**producer** | **str** |  | 
**kbacategory** | **str** |  | [optional] 
**element_name** | **str** |  | [optional] 

## Example

```python
from gbs3api.models.vehicle_type import VehicleType

# TODO update the JSON string below
json = "{}"
# create an instance of VehicleType from a JSON string
vehicle_type_instance = VehicleType.from_json(json)
# print the JSON string representation of the object
print(VehicleType.to_json())

# convert the object into a dict
vehicle_type_dict = vehicle_type_instance.to_dict()
# create an instance of VehicleType from a dict
vehicle_type_from_dict = VehicleType.from_dict(vehicle_type_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


