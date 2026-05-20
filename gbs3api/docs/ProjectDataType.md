# ProjectDataType


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**path** | **str** |  | [optional] 
**company** | **str** |  | 
**name** | **str** |  | [optional] 
**customer_name** | **str** |  | [optional] 
**language** | **str** |  | 
**function_number** | **str** |  | 
**wbs_element** | **str** |  | [optional] 
**remark** | **str** |  | [optional] 
**vehicle_type** | [**VehicleType**](VehicleType.md) |  | 
**test_series** | [**List[TestSeriesDataType]**](TestSeriesDataType.md) |  | [optional] 
**additional_group** | [**List[AdditionalGroup]**](AdditionalGroup.md) |  | [optional] 
**element_name** | **str** |  | [optional] 

## Example

```python
from gbs3api.models.project_data_type import ProjectDataType

# TODO update the JSON string below
json = "{}"
# create an instance of ProjectDataType from a JSON string
project_data_type_instance = ProjectDataType.from_json(json)
# print the JSON string representation of the object
print(ProjectDataType.to_json())

# convert the object into a dict
project_data_type_dict = project_data_type_instance.to_dict()
# create an instance of ProjectDataType from a dict
project_data_type_from_dict = ProjectDataType.from_dict(project_data_type_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


