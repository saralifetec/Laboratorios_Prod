# SensorGroupType


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**path** | **str** |  | [optional] 
**supplier** | **str** |  | 
**model** | **str** |  | 
**description** | **str** |  | [optional] 
**excitation_voltage_max** | **float** |  | [optional] 
**self_descriptive** | **bool** |  | [optional] 
**category** | **str** |  | [optional] 
**main_category** | **str** |  | 
**validation** | [**ValidationType**](ValidationType.md) |  | [optional] 
**sensor_type** | [**List[SensorType]**](SensorType.md) |  | [optional] 
**element_name** | **str** |  | [optional] 

## Example

```python
from gbs3api.models.sensor_group_type import SensorGroupType

# TODO update the JSON string below
json = "{}"
# create an instance of SensorGroupType from a JSON string
sensor_group_type_instance = SensorGroupType.from_json(json)
# print the JSON string representation of the object
print(SensorGroupType.to_json())

# convert the object into a dict
sensor_group_type_dict = sensor_group_type_instance.to_dict()
# create an instance of SensorGroupType from a dict
sensor_group_type_from_dict = SensorGroupType.from_dict(sensor_group_type_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


