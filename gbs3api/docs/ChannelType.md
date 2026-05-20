# ChannelType


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**path** | **str** |  | [optional] 
**channel_code** | **str** |  | 
**unit** | **str** |  | 
**sensor_group_id** | **str** |  | 
**sensor_group_type** | **str** |  | 
**pre_filter_type** | **str** |  | 
**cut_off_frequency** | **str** |  | 
**channel_amplitude_class** | **str** |  | 
**data_source** | **str** |  | 
**data_status** | **str** |  | 
**sampling_interval** | **str** |  | 
**bit_resolution** | **str** |  | 
**time_of_first_sample** | **str** |  | 
**number_of_samples** | **str** |  | 
**first_global_maximum_value** | **str** |  | 
**time_of_maximum_value** | **str** |  | 
**first_global_minimum_value** | **str** |  | 
**time_of_minimum_value** | **str** |  | 
**index** | **str** |  | [optional] 
**source** | **str** |  | [optional] 
**sensor_group** | [**SensorGroup**](SensorGroup.md) |  | [optional] 
**results** | [**List[ResultsType]**](ResultsType.md) |  | [optional] 
**preview** | [**ImageType**](ImageType.md) |  | [optional] 
**additional_group** | [**List[AdditionalGroup]**](AdditionalGroup.md) |  | [optional] 
**element_name** | **str** |  | [optional] 

## Example

```python
from gbs3api.models.channel_type import ChannelType

# TODO update the JSON string below
json = "{}"
# create an instance of ChannelType from a JSON string
channel_type_instance = ChannelType.from_json(json)
# print the JSON string representation of the object
print(ChannelType.to_json())

# convert the object into a dict
channel_type_dict = channel_type_instance.to_dict()
# create an instance of ChannelType from a dict
channel_type_from_dict = ChannelType.from_dict(channel_type_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


