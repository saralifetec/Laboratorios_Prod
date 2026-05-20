# MatrixStepDto


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**test_name** | **str** |  | [optional] 
**vpnr_pos** | **int** |  | [optional] 
**intention** | **str** |  | [optional] 
**remark** | **str** |  | [optional] 
**comment** | **str** |  | [optional] 
**rating** | **str** |  | [optional] 
**total_parts** | **int** |  | [optional] 
**reference_test_id** | **int** |  | [optional] 
**component_groups** | [**List[ComponentGroupDto]**](ComponentGroupDto.md) |  | [optional] 

## Example

```python
from gbs3api.models.matrix_step_dto import MatrixStepDto

# TODO update the JSON string below
json = "{}"
# create an instance of MatrixStepDto from a JSON string
matrix_step_dto_instance = MatrixStepDto.from_json(json)
# print the JSON string representation of the object
print(MatrixStepDto.to_json())

# convert the object into a dict
matrix_step_dto_dict = matrix_step_dto_instance.to_dict()
# create an instance of MatrixStepDto from a dict
matrix_step_dto_from_dict = MatrixStepDto.from_dict(matrix_step_dto_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


