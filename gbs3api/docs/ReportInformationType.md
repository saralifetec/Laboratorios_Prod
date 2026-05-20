# ReportInformationType


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**path** | **str** |  | [optional] 
**source** | **str** |  | [optional] 
**additional_group** | [**List[AdditionalGroup]**](AdditionalGroup.md) |  | [optional] 
**element_name** | **str** |  | [optional] 

## Example

```python
from gbs3api.models.report_information_type import ReportInformationType

# TODO update the JSON string below
json = "{}"
# create an instance of ReportInformationType from a JSON string
report_information_type_instance = ReportInformationType.from_json(json)
# print the JSON string representation of the object
print(ReportInformationType.to_json())

# convert the object into a dict
report_information_type_dict = report_information_type_instance.to_dict()
# create an instance of ReportInformationType from a dict
report_information_type_from_dict = ReportInformationType.from_dict(report_information_type_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


