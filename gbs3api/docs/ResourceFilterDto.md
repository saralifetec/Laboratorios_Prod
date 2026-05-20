# ResourceFilterDto


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**id** | **int** |  | [optional] 
**name** | **str** |  | [optional] 
**user** | **str** |  | [optional] 
**teams** | **List[int]** |  | [optional] 
**locations** | **List[int]** |  | [optional] 
**resource_types** | **List[int]** |  | [optional] 
**interval** | **int** |  | [optional] 

## Example

```python
from gbs3api.models.resource_filter_dto import ResourceFilterDto

# TODO update the JSON string below
json = "{}"
# create an instance of ResourceFilterDto from a JSON string
resource_filter_dto_instance = ResourceFilterDto.from_json(json)
# print the JSON string representation of the object
print(ResourceFilterDto.to_json())

# convert the object into a dict
resource_filter_dto_dict = resource_filter_dto_instance.to_dict()
# create an instance of ResourceFilterDto from a dict
resource_filter_dto_from_dict = ResourceFilterDto.from_dict(resource_filter_dto_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


