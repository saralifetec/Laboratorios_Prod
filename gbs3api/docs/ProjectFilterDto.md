# ProjectFilterDto


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**id** | **int** |  | [optional] 
**name** | **str** |  | [optional] 
**user** | **str** |  | [optional] 
**teams** | **List[int]** |  | [optional] 
**locations** | **List[int]** |  | [optional] 
**statuses** | **List[str]** |  | [optional] 
**interval** | **int** |  | [optional] 

## Example

```python
from gbs3api.models.project_filter_dto import ProjectFilterDto

# TODO update the JSON string below
json = "{}"
# create an instance of ProjectFilterDto from a JSON string
project_filter_dto_instance = ProjectFilterDto.from_json(json)
# print the JSON string representation of the object
print(ProjectFilterDto.to_json())

# convert the object into a dict
project_filter_dto_dict = project_filter_dto_instance.to_dict()
# create an instance of ProjectFilterDto from a dict
project_filter_dto_from_dict = ProjectFilterDto.from_dict(project_filter_dto_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


