# ValueDto


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**name** | **str** |  | [optional] 
**value_list** | **str** |  | [optional] 
**description** | **str** |  | [optional] 
**index** | **int** |  | [optional] 

## Example

```python
from gbs4api.models.value_dto import ValueDto

# TODO update the JSON string below
json = "{}"
# create an instance of ValueDto from a JSON string
value_dto_instance = ValueDto.from_json(json)
# print the JSON string representation of the object
print(ValueDto.to_json())

# convert the object into a dict
value_dto_dict = value_dto_instance.to_dict()
# create an instance of ValueDto from a dict
value_dto_from_dict = ValueDto.from_dict(value_dto_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


