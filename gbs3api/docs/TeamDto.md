# TeamDto


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**id** | **int** |  | [optional] 
**name** | **str** |  | [optional] 
**description** | **str** |  | [optional] 
**users** | **List[str]** |  | [optional] 

## Example

```python
from gbs3api.models.team_dto import TeamDto

# TODO update the JSON string below
json = "{}"
# create an instance of TeamDto from a JSON string
team_dto_instance = TeamDto.from_json(json)
# print the JSON string representation of the object
print(TeamDto.to_json())

# convert the object into a dict
team_dto_dict = team_dto_instance.to_dict()
# create an instance of TeamDto from a dict
team_dto_from_dict = TeamDto.from_dict(team_dto_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


