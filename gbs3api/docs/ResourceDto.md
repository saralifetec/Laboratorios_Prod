# ResourceDto


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**id** | **int** |  | [optional] 
**data_id** | **int** |  | [optional] 
**label** | **str** |  | [optional] 
**name** | **str** |  | [optional] 
**resource_type** | **int** |  | [optional] 
**location** | **int** |  | [optional] 
**info** | **str** |  | [optional] 
**status** | **str** |  | [optional] 
**resource_class** | **str** |  | [optional] 

## Example

```python
from gbs3api.models.resource_dto import ResourceDto

# TODO update the JSON string below
json = "{}"
# create an instance of ResourceDto from a JSON string
resource_dto_instance = ResourceDto.from_json(json)
# print the JSON string representation of the object
print(ResourceDto.to_json())

# convert the object into a dict
resource_dto_dict = resource_dto_instance.to_dict()
# create an instance of ResourceDto from a dict
resource_dto_from_dict = ResourceDto.from_dict(resource_dto_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


