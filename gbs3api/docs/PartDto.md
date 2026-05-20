# PartDto


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**part_id** | **int** |  | [optional] 
**test_number** | **str** |  | [optional] 
**part_name** | **str** |  | [optional] 
**part_number** | **str** |  | [optional] 
**customer_part_number** | **str** |  | [optional] 
**description** | **str** |  | [optional] 
**bom** | [**BomDto**](BomDto.md) |  | [optional] 

## Example

```python
from gbs3api.models.part_dto import PartDto

# TODO update the JSON string below
json = "{}"
# create an instance of PartDto from a JSON string
part_dto_instance = PartDto.from_json(json)
# print the JSON string representation of the object
print(PartDto.to_json())

# convert the object into a dict
part_dto_dict = part_dto_instance.to_dict()
# create an instance of PartDto from a dict
part_dto_from_dict = PartDto.from_dict(part_dto_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


