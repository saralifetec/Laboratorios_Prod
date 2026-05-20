# CommentDto


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**id** | **int** |  | [optional] 
**user** | **str** |  | 
**creation** | **datetime** |  | 
**text** | **str** |  | 

## Example

```python
from gbs4api.models.comment_dto import CommentDto

# TODO update the JSON string below
json = "{}"
# create an instance of CommentDto from a JSON string
comment_dto_instance = CommentDto.from_json(json)
# print the JSON string representation of the object
print(CommentDto.to_json())

# convert the object into a dict
comment_dto_dict = comment_dto_instance.to_dict()
# create an instance of CommentDto from a dict
comment_dto_from_dict = CommentDto.from_dict(comment_dto_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


