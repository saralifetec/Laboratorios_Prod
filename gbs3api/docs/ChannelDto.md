# ChannelDto


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**channel_code** | **str** |  | 
**description** | **str** |  | [optional] 
**max_range** | **float** |  | [optional] 
**min_range** | **float** |  | [optional] 
**position_index** | **int** |  | 
**direction** | **str** |  | [optional] 
**channel_group** | **str** |  | 
**equipment** | **str** |  | 
**polarity** | **str** |  | 

## Example

```python
from gbs3api.models.channel_dto import ChannelDto

# TODO update the JSON string below
json = "{}"
# create an instance of ChannelDto from a JSON string
channel_dto_instance = ChannelDto.from_json(json)
# print the JSON string representation of the object
print(ChannelDto.to_json())

# convert the object into a dict
channel_dto_dict = channel_dto_instance.to_dict()
# create an instance of ChannelDto from a dict
channel_dto_from_dict = ChannelDto.from_dict(channel_dto_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


