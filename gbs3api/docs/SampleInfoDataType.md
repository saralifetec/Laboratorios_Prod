# SampleInfoDataType


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**path** | **str** |  | [optional] 
**sample_id** | **str** |  | 
**status** | **str** |  | [optional] 
**number** | **str** |  | [optional] 
**remark** | **str** |  | [optional] 
**warehouse** | **str** |  | [optional] 
**module_serieal_number** | **str** |  | [optional] 
**inflator_serieal_number** | **str** |  | [optional] 
**is_out_side** | **int** |  | [optional] 
**location** | **str** |  | [optional] 
**responsible_person** | **str** |  | [optional] 
**checked_in_by** | **str** |  | [optional] 
**photo** | [**List[ImageType]**](ImageType.md) |  | [optional] 
**additional_group** | [**List[AdditionalGroup]**](AdditionalGroup.md) |  | [optional] 
**prnumber** | **str** |  | [optional] 
**element_name** | **str** |  | [optional] 

## Example

```python
from gbs3api.models.sample_info_data_type import SampleInfoDataType

# TODO update the JSON string below
json = "{}"
# create an instance of SampleInfoDataType from a JSON string
sample_info_data_type_instance = SampleInfoDataType.from_json(json)
# print the JSON string representation of the object
print(SampleInfoDataType.to_json())

# convert the object into a dict
sample_info_data_type_dict = sample_info_data_type_instance.to_dict()
# create an instance of SampleInfoDataType from a dict
sample_info_data_type_from_dict = SampleInfoDataType.from_dict(sample_info_data_type_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


