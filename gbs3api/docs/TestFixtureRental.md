# TestFixtureRental


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**path** | **str** |  | [optional] 
**rental_date** | **datetime** |  | 
**return_date** | **datetime** |  | [optional] 
**target_date** | **datetime** |  | [optional] 
**contact_name** | **str** |  | 
**contact_phone** | **str** |  | 
**contact_fax** | **str** |  | 
**contact_email** | **str** |  | 
**description** | **str** |  | [optional] 
**lender** | **str** |  | 
**hour_period** | **int** |  | [optional] 
**day_period** | **int** |  | [optional] 
**month_period** | **int** |  | [optional] 
**indefinite_period** | **bool** |  | [optional] 
**extend_loan_count** | **int** |  | [optional] 
**element_name** | **str** |  | [optional] 

## Example

```python
from gbs3api.models.test_fixture_rental import TestFixtureRental

# TODO update the JSON string below
json = "{}"
# create an instance of TestFixtureRental from a JSON string
test_fixture_rental_instance = TestFixtureRental.from_json(json)
# print the JSON string representation of the object
print(TestFixtureRental.to_json())

# convert the object into a dict
test_fixture_rental_dict = test_fixture_rental_instance.to_dict()
# create an instance of TestFixtureRental from a dict
test_fixture_rental_from_dict = TestFixtureRental.from_dict(test_fixture_rental_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


