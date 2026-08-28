# ImageType


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**path** | **str** |  | [optional] 
**source** | **str** |  | [optional] 
**id_number** | **str** |  | [optional] 
**test_object_number** | **str** |  | [optional] 
**camery_type** | **str** |  | [optional] 
**test_type** | **str** |  | [optional] 
**description** | **str** |  | [optional] 
**direction** | **str** |  | [optional] 
**aperture** | **str** |  | [optional] 
**exposure_time** | **str** |  | [optional] 
**width** | **str** |  | [optional] 
**height** | **str** |  | [optional] 
**aspect_ratio** | **str** |  | [optional] 
**color** | **str** |  | [optional] 
**file_name** | **str** |  | 
**file_data** | **bytearray** |  | 
**format** | **str** |  | [optional] 
**compression** | **str** |  | [optional] 
**additional_group** | [**List[AdditionalGroup]**](AdditionalGroup.md) |  | [optional] 
**element_name** | **str** |  | [optional] 

## Example

```python
from gbs3api.models.image_type import ImageType

# TODO update the JSON string below
json = "{}"
# create an instance of ImageType from a JSON string
image_type_instance = ImageType.from_json(json)
# print the JSON string representation of the object
print(ImageType.to_json())

# convert the object into a dict
image_type_dict = image_type_instance.to_dict()
# create an instance of ImageType from a dict
image_type_from_dict = ImageType.from_dict(image_type_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


