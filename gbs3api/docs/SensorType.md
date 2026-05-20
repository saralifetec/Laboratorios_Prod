# SensorType


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**path** | **str** |  | [optional] 
**physical_dimension** | **str** |  | 
**physical_unit** | **str** |  | 
**axis_direction** | **str** |  | 
**min_range** | **float** |  | [optional] 
**max_range** | **float** |  | [optional] 
**description** | **str** |  | [optional] 
**max_linearity_deviation** | **float** |  | [optional] 
**entry_resistance** | **float** |  | [optional] 
**output_resistance** | **float** |  | [optional] 
**bridge_type** | **str** |  | 
**channel_type** | **str** |  | 
**operating_principle** | **str** |  | 
**offset** | **float** |  | [optional] 
**offset_tol** | **float** |  | [optional] 
**validation** | [**ValidationType**](ValidationType.md) |  | [optional] 
**element_name** | **str** |  | [optional] 

## Example

```python
from gbs3api.models.sensor_type import SensorType

# TODO update the JSON string below
json = "{}"
# create an instance of SensorType from a JSON string
sensor_type_instance = SensorType.from_json(json)
# print the JSON string representation of the object
print(SensorType.to_json())

# convert the object into a dict
sensor_type_dict = sensor_type_instance.to_dict()
# create an instance of SensorType from a dict
sensor_type_from_dict = SensorType.from_dict(sensor_type_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


