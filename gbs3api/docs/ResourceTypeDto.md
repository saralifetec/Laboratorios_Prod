# ResourceTypeDto


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**id** | **int** |  | [optional] 
**data_id** | **int** |  | [optional] 
**class_name** | **str** |  | [optional] 
**name** | **str** |  | [optional] 
**schedule_types** | **List[int]** |  | [optional] 
**resources** | **List[int]** |  | [optional] 

## Example

```python
from gbs3api.models.resource_type_dto import ResourceTypeDto

# TODO update the JSON string below
json = "{}"
# create an instance of ResourceTypeDto from a JSON string
resource_type_dto_instance = ResourceTypeDto.from_json(json)
# print the JSON string representation of the object
print(ResourceTypeDto.to_json())

# convert the object into a dict
resource_type_dto_dict = resource_type_dto_instance.to_dict()
# create an instance of ResourceTypeDto from a dict
resource_type_dto_from_dict = ResourceTypeDto.from_dict(resource_type_dto_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


