# DocumentInformationType


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**path** | **str** |  | [optional] 
**source** | **str** |  | [optional] 
**additional_group** | [**List[AdditionalGroup]**](AdditionalGroup.md) |  | [optional] 
**element_name** | **str** |  | [optional] 

## Example

```python
from gbs3api.models.document_information_type import DocumentInformationType

# TODO update the JSON string below
json = "{}"
# create an instance of DocumentInformationType from a JSON string
document_information_type_instance = DocumentInformationType.from_json(json)
# print the JSON string representation of the object
print(DocumentInformationType.to_json())

# convert the object into a dict
document_information_type_dict = document_information_type_instance.to_dict()
# create an instance of DocumentInformationType from a dict
document_information_type_from_dict = DocumentInformationType.from_dict(document_information_type_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


