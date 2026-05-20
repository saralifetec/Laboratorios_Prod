# ChannelGroupDto


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**uuid** | **str** |  | [optional] 
**name** | **str** |  | 
**description** | **str** |  | [optional] 
**label** | **str** |  | [optional] 
**calibration_category** | **str** |  | [optional] 
**status** | **str** |  | [optional] 
**maintenance_category** | **str** |  | [optional] 
**parent** | **str** |  | [optional] 
**children** | **List[str]** |  | [optional] 
**channels** | **List[str]** |  | [optional] 
**channel_group_type** | **str** |  | 
**location** | **int** |  | 
**responsible_user_group** | **str** |  | [optional] 
**display_name** | **str** |  | 
**shot_count** | **int** |  | [optional] 

## Example

```python
from gbs3api.models.channel_group_dto import ChannelGroupDto

# TODO update the JSON string below
json = "{}"
# create an instance of ChannelGroupDto from a JSON string
channel_group_dto_instance = ChannelGroupDto.from_json(json)
# print the JSON string representation of the object
print(ChannelGroupDto.to_json())

# convert the object into a dict
channel_group_dto_dict = channel_group_dto_instance.to_dict()
# create an instance of ChannelGroupDto from a dict
channel_group_dto_from_dict = ChannelGroupDto.from_dict(channel_group_dto_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


