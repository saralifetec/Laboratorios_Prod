# Bom


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**path** | **str** |  | [optional] 
**bom** | **str** |  | [optional] 
**order** | **str** |  | [optional] 
**found_in_test_series** | **str** |  | [optional] 
**material** | **str** |  | [optional] 
**item_number** | **str** |  | [optional] 
**item_text** | **str** |  | [optional] 
**item_category** | **str** |  | [optional] 
**component_number** | **str** |  | [optional] 
**material_description_en** | **str** |  | [optional] 
**material_description_de** | **str** |  | [optional] 
**material_description_es** | **str** |  | [optional] 
**plant** | **str** |  | [optional] 
**entry_quantity** | **float** |  | [optional] 
**source_system_key** | **str** |  | [optional] 
**bom_elements** | [**List[Bom]**](Bom.md) |  | [optional] 
**element_name** | **str** |  | [optional] 

## Example

```python
from gbs3api.models.bom import Bom

# TODO update the JSON string below
json = "{}"
# create an instance of Bom from a JSON string
bom_instance = Bom.from_json(json)
# print the JSON string representation of the object
print(Bom.to_json())

# convert the object into a dict
bom_dict = bom_instance.to_dict()
# create an instance of Bom from a dict
bom_from_dict = Bom.from_dict(bom_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


