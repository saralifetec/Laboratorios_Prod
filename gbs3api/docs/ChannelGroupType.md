# ChannelGroupType


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**path** | **str** |  | [optional] 
**name** | **str** |  | 
**sub_channel** | [**List[ChannelGroupType]**](ChannelGroupType.md) |  | [optional] 
**channel** | [**List[ChannelType]**](ChannelType.md) |  | [optional] 
**element_name** | **str** |  | [optional] 

## Example

```python
from gbs3api.models.channel_group_type import ChannelGroupType

# TODO update the JSON string below
json = "{}"
# create an instance of ChannelGroupType from a JSON string
channel_group_type_instance = ChannelGroupType.from_json(json)
# print the JSON string representation of the object
print(ChannelGroupType.to_json())

# convert the object into a dict
channel_group_type_dict = channel_group_type_instance.to_dict()
# create an instance of ChannelGroupType from a dict
channel_group_type_from_dict = ChannelGroupType.from_dict(channel_group_type_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


