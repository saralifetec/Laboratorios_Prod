# LocationDto


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**id** | **int** |  | [optional] 
**name** | **str** |  | [optional] 
**label** | **str** |  | [optional] 
**description** | **str** |  | [optional] 
**parent_id** | **int** |  | [optional] 
**category** | **str** |  | [optional] 
**children** | **List[int]** |  | [optional] 
**available_for_test_catalog** | **bool** |  | [optional] 

## Example

```python
from gbs4api.models.location_dto import LocationDto

# TODO update the JSON string below
json = "{}"
# create an instance of LocationDto from a JSON string
location_dto_instance = LocationDto.from_json(json)
# print the JSON string representation of the object
print(LocationDto.to_json())

# convert the object into a dict
location_dto_dict = location_dto_instance.to_dict()
# create an instance of LocationDto from a dict
location_dto_from_dict = LocationDto.from_dict(location_dto_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


