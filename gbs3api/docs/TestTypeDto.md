# TestTypeDto


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**id** | **int** |  | [optional] 
**name** | **str** |  | [optional] 
**description** | **str** |  | [optional] 
**sub_types** | **List[int]** |  | [optional] 
**test_matrix_definitions** | **List[int]** |  | [optional] 
**category** | **str** |  | [optional] 
**role** | **str** |  | [optional] 
**default** | **bool** |  | [optional] 

## Example

```python
from gbs3api.models.test_type_dto import TestTypeDto

# TODO update the JSON string below
json = "{}"
# create an instance of TestTypeDto from a JSON string
test_type_dto_instance = TestTypeDto.from_json(json)
# print the JSON string representation of the object
print(TestTypeDto.to_json())

# convert the object into a dict
test_type_dto_dict = test_type_dto_instance.to_dict()
# create an instance of TestTypeDto from a dict
test_type_dto_from_dict = TestTypeDto.from_dict(test_type_dto_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


