# ValueListDto


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**name** | **str** |  | 
**description** | **str** |  | [optional] 

## Example

```python
from gbs3api.models.value_list_dto import ValueListDto

# TODO update the JSON string below
json = "{}"
# create an instance of ValueListDto from a JSON string
value_list_dto_instance = ValueListDto.from_json(json)
# print the JSON string representation of the object
print(ValueListDto.to_json())

# convert the object into a dict
value_list_dto_dict = value_list_dto_instance.to_dict()
# create an instance of ValueListDto from a dict
value_list_dto_from_dict = ValueListDto.from_dict(value_list_dto_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


