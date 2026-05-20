# SampleDataType


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**path** | **str** |  | [optional] 
**position_number** | **str** |  | 
**sample_id** | **str** |  | 
**customer_part_number** | **str** |  | [optional] 
**amount** | **int** |  | [optional] 
**remark** | **str** |  | [optional] 
**software** | **str** |  | [optional] 
**version** | **str** |  | [optional] 
**unloading_place** | **str** |  | [optional] 
**part_name** | **str** |  | [optional] 
**ebom** | **str** |  | [optional] 
**manufacturer** | **str** |  | [optional] 
**manufacturer_number** | **str** |  | [optional] 
**manufacturer_number_version** | **str** |  | [optional] 
**customer_version** | **str** |  | [optional] 
**warehouse_id** | **str** |  | [optional] 
**source_id** | **str** |  | [optional] 
**sample_info** | [**SampleInfoDataType**](SampleInfoDataType.md) |  | [optional] 
**sample_type** | [**SampleTypeDataType**](SampleTypeDataType.md) |  | [optional] 
**location** | **str** |  | [optional] 
**is_deleted** | **bool** |  | [optional] 
**prototype_sort_index** | **int** |  | [optional] 
**sample_elements** | [**List[SampleElementDataType]**](SampleElementDataType.md) |  | [optional] 
**additional_group** | [**List[AdditionalGroup]**](AdditionalGroup.md) |  | [optional] 
**element_name** | **str** |  | [optional] 
**pbsfin_good_id** | **str** |  | [optional] 

## Example

```python
from gbs3api.models.sample_data_type import SampleDataType

# TODO update the JSON string below
json = "{}"
# create an instance of SampleDataType from a JSON string
sample_data_type_instance = SampleDataType.from_json(json)
# print the JSON string representation of the object
print(SampleDataType.to_json())

# convert the object into a dict
sample_data_type_dict = sample_data_type_instance.to_dict()
# create an instance of SampleDataType from a dict
sample_data_type_from_dict = SampleDataType.from_dict(sample_data_type_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


