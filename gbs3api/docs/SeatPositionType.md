# SeatPositionType


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**path** | **str** |  | [optional] 
**channel** | [**List[ChannelType]**](ChannelType.md) |  | [optional] 
**channel_group** | [**List[ChannelGroupType]**](ChannelGroupType.md) |  | [optional] 
**additional_group** | [**List[AdditionalGroup]**](AdditionalGroup.md) |  | [optional] 
**iso_code** | **str** |  | [optional] 
**element_name** | **str** |  | [optional] 

## Example

```python
from gbs3api.models.seat_position_type import SeatPositionType

# TODO update the JSON string below
json = "{}"
# create an instance of SeatPositionType from a JSON string
seat_position_type_instance = SeatPositionType.from_json(json)
# print the JSON string representation of the object
print(SeatPositionType.to_json())

# convert the object into a dict
seat_position_type_dict = seat_position_type_instance.to_dict()
# create an instance of SeatPositionType from a dict
seat_position_type_from_dict = SeatPositionType.from_dict(seat_position_type_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


