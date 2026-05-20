# PhotoInformationType


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**path** | **str** |  | [optional] 
**number_of_photos** | **int** |  | [optional] 
**source** | **str** |  | [optional] 
**photo** | [**List[ImageType]**](ImageType.md) |  | [optional] 
**additional_group** | [**List[AdditionalGroup]**](AdditionalGroup.md) |  | [optional] 
**element_name** | **str** |  | [optional] 

## Example

```python
from gbs3api.models.photo_information_type import PhotoInformationType

# TODO update the JSON string below
json = "{}"
# create an instance of PhotoInformationType from a JSON string
photo_information_type_instance = PhotoInformationType.from_json(json)
# print the JSON string representation of the object
print(PhotoInformationType.to_json())

# convert the object into a dict
photo_information_type_dict = photo_information_type_instance.to_dict()
# create an instance of PhotoInformationType from a dict
photo_information_type_from_dict = PhotoInformationType.from_dict(photo_information_type_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


