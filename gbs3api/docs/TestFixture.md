# TestFixture


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**path** | **str** |  | [optional] 
**number** | **str** |  | 
**local_number** | **str** |  | 
**description** | **str** |  | [optional] 
**creation_date** | **datetime** |  | [optional] 
**scrapping_date** | **datetime** |  | [optional] 
**cost_center** | **str** |  | [optional] 
**count** | **int** |  | [optional] 
**cost** | **float** |  | [optional] 
**release_number** | **str** |  | [optional] 
**test_fixture_type** | [**TestFixtureType**](TestFixtureType.md) |  | 
**company** | **str** |  | 
**location** | **str** |  | 
**contact_name** | **str** |  | [optional] 
**contact_phone** | **str** |  | [optional] 
**contact_fax** | **str** |  | [optional] 
**contact_email** | **str** |  | [optional] 
**used** | **int** |  | [optional] 
**storage_position** | **str** |  | [optional] 
**weight** | **float** |  | [optional] 
**resource_type_scheduling** | **str** |  | [optional] 
**resource_type_scheduling_id** | **str** |  | [optional] 
**status** | **str** |  | 
**sub_test_fixture** | [**List[TestFixture]**](TestFixture.md) |  | [optional] 
**additional_group** | [**List[AdditionalGroup]**](AdditionalGroup.md) |  | [optional] 
**photo** | [**List[ImageType]**](ImageType.md) |  | [optional] 
**design_drawing** | [**List[TestFixtureDesignDrawing]**](TestFixtureDesignDrawing.md) |  | [optional] 
**rental** | [**List[TestFixtureRental]**](TestFixtureRental.md) |  | [optional] 
**status_comment** | [**List[TestFixtureStatusComment]**](TestFixtureStatusComment.md) |  | [optional] 
**history_log** | [**List[TestFixtureHistoryLog]**](TestFixtureHistoryLog.md) |  | [optional] 
**element_name** | **str** |  | [optional] 

## Example

```python
from gbs3api.models.test_fixture import TestFixture

# TODO update the JSON string below
json = "{}"
# create an instance of TestFixture from a JSON string
test_fixture_instance = TestFixture.from_json(json)
# print the JSON string representation of the object
print(TestFixture.to_json())

# convert the object into a dict
test_fixture_dict = test_fixture_instance.to_dict()
# create an instance of TestFixture from a dict
test_fixture_from_dict = TestFixture.from_dict(test_fixture_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


