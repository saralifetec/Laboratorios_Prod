# GeneralInformationType


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**path** | **str** |  | [optional] 
**test_number** | **str** |  | 
**is_active** | **bool** |  | [optional] 
**is_test_step** | **bool** |  | [optional] 
**version** | **int** |  | [optional] 
**test_category** | **str** |  | [optional] 
**name** | **str** |  | [optional] 
**test_step_layout** | [**TestStepLayout**](TestStepLayout.md) |  | [optional] 
**samples** | **str** |  | [optional] 
**laboratory_name** | **str** |  | 
**laboratory_contact_name** | **str** |  | [optional] 
**laboratory_contact_phone** | **str** |  | [optional] 
**laboratory_contact_fax** | **str** |  | [optional] 
**laboratory_contact_email** | **str** |  | [optional] 
**laboratory_test_ref_number** | **str** |  | 
**requestor_name** | **str** |  | [optional] 
**requestor_phone** | **str** |  | [optional] 
**currently_logged_user** | **str** |  | [optional] 
**proxy_contact_name** | **str** |  | [optional] 
**proxy_contact_phone** | **str** |  | [optional] 
**responsible_location** | **str** |  | [optional] 
**responsible_location_address** | **str** |  | [optional] 
**proxy_contact_fax** | **str** |  | [optional] 
**proxy_contact_email** | **str** |  | [optional] 
**customer_name** | **str** |  | 
**customer_test_ref_number** | **str** |  | 
**customer_project_ref_number** | **str** |  | [optional] 
**customer_order_number** | **str** |  | [optional] 
**customer_cost_unit** | **str** |  | [optional] 
**customer_test_engineer_name** | **str** |  | [optional] 
**customer_test_engineer_phone** | **str** |  | [optional] 
**customer_test_engineer_fax** | **str** |  | [optional] 
**customer_test_engineer_email** | **str** |  | [optional] 
**title** | **str** |  | 
**type_of_the_test** | **str** |  | 
**subtype_of_the_test** | **str** |  | 
**template_name** | **str** |  | 
**regulation** | **str** |  | [optional] 
**reference_temperature** | **str** |  | [optional] 
**relative_air_humidity** | **str** |  | [optional] 
**date_of_the_test** | **datetime** |  | 
**estimated_start** | **datetime** |  | [optional] 
**estimated_end** | **datetime** |  | [optional] 
**actual_end** | **datetime** |  | [optional] 
**order_date** | **datetime** |  | [optional] 
**deadline_lab** | **datetime** |  | [optional] 
**instrumentation_standard** | **str** |  | [optional] 
**test_bench** | **str** |  | [optional] 
**intention** | **str** |  | [optional] 
**customer_visit** | **bool** |  | [optional] 
**customer_visit_telephone_number** | **str** |  | [optional] 
**remark** | **str** |  | [optional] 
**location** | **str** |  | [optional] 
**status** | **str** |  | [optional] 
**execution_status** | **str** |  | [optional] 
**work_time** | **int** |  | [optional] 
**work_time_start** | **datetime** |  | [optional] 
**skill_id_list** | **str** |  | [optional] 
**work_instruction** | [**List[WorkInstruction]**](WorkInstruction.md) |  | [optional] 
**test_fixture** | [**List[TestFixture]**](TestFixture.md) |  | [optional] 
**sample** | [**List[SampleDataType]**](SampleDataType.md) |  | [optional] 
**sub_tests** | [**List[TestDataType]**](TestDataType.md) |  | [optional] 
**test_object** | [**List[TestObjectType]**](TestObjectType.md) |  | [optional] 
**additional_group** | [**List[AdditionalGroup]**](AdditionalGroup.md) |  | [optional] 
**source** | **str** |  | [optional] 
**diagram** | [**DiagramInformationType**](DiagramInformationType.md) |  | [optional] 
**document** | [**DocumentInformationType**](DocumentInformationType.md) |  | [optional] 
**movie** | [**MovieInformationType**](MovieInformationType.md) |  | [optional] 
**photo** | [**PhotoInformationType**](PhotoInformationType.md) |  | [optional] 
**raw** | [**RawInformationType**](RawInformationType.md) |  | [optional] 
**report** | [**ReportInformationType**](ReportInformationType.md) |  | [optional] 
**statics** | [**StaticInformationType**](StaticInformationType.md) |  | [optional] 
**additional** | [**AdditionalInformationType**](AdditionalInformationType.md) |  | [optional] 
**component_test_group** | [**ComponentTestGroupType**](ComponentTestGroupType.md) |  | [optional] 
**parts_group** | [**List[PartsGroup]**](PartsGroup.md) |  | [optional] 
**vpn_r_pos** | **str** |  | [optional] 
**element_name** | **str** |  | [optional] 
**sapnetplan** | **str** |  | [optional] 

## Example

```python
from gbs3api.models.general_information_type import GeneralInformationType

# TODO update the JSON string below
json = "{}"
# create an instance of GeneralInformationType from a JSON string
general_information_type_instance = GeneralInformationType.from_json(json)
# print the JSON string representation of the object
print(GeneralInformationType.to_json())

# convert the object into a dict
general_information_type_dict = general_information_type_instance.to_dict()
# create an instance of GeneralInformationType from a dict
general_information_type_from_dict = GeneralInformationType.from_dict(general_information_type_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


