# SubTestTypeDto


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**name** | **str** |  | [optional] 
**description** | **str** |  | [optional] 

## Example

```python
from gbs4api.models.sub_test_type_dto import SubTestTypeDto

# TODO update the JSON string below
json = "{}"
# create an instance of SubTestTypeDto from a JSON string
sub_test_type_dto_instance = SubTestTypeDto.from_json(json)
# print the JSON string representation of the object
print(SubTestTypeDto.to_json())

# convert the object into a dict
sub_test_type_dto_dict = sub_test_type_dto_instance.to_dict()
# create an instance of SubTestTypeDto from a dict
sub_test_type_dto_from_dict = SubTestTypeDto.from_dict(sub_test_type_dto_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


