# ChannelGroupTypeDto


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**name** | **str** |  | [optional] 
**description** | **str** |  | [optional] 
**label** | **str** |  | [optional] 
**parent** | **str** |  | [optional] 
**children** | **List[str]** |  | [optional] 
**channel_groups** | **List[str]** |  | [optional] 
**resource_type_enabled** | **bool** |  | [optional] 

## Example

```python
from gbs3api.models.channel_group_type_dto import ChannelGroupTypeDto

# TODO update the JSON string below
json = "{}"
# create an instance of ChannelGroupTypeDto from a JSON string
channel_group_type_dto_instance = ChannelGroupTypeDto.from_json(json)
# print the JSON string representation of the object
print(ChannelGroupTypeDto.to_json())

# convert the object into a dict
channel_group_type_dto_dict = channel_group_type_dto_instance.to_dict()
# create an instance of ChannelGroupTypeDto from a dict
channel_group_type_dto_from_dict = ChannelGroupTypeDto.from_dict(channel_group_type_dto_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


