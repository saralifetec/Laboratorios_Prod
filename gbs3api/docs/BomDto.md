# BomDto


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**bom_id** | **int** |  | [optional] 
**material** | **str** |  | [optional] 
**material_description** | **str** |  | [optional] 
**plant** | **str** |  | [optional] 
**item_number** | **str** |  | [optional] 
**item_category** | **str** |  | [optional] 
**source_system_key** | **str** |  | [optional] 
**bom_elements** | [**List[BomDto]**](BomDto.md) |  | [optional] 

## Example

```python
from gbs3api.models.bom_dto import BomDto

# TODO update the JSON string below
json = "{}"
# create an instance of BomDto from a JSON string
bom_dto_instance = BomDto.from_json(json)
# print the JSON string representation of the object
print(BomDto.to_json())

# convert the object into a dict
bom_dto_dict = bom_dto_instance.to_dict()
# create an instance of BomDto from a dict
bom_dto_from_dict = BomDto.from_dict(bom_dto_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


