# PersonDto


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**person_id** | **int** |  | [optional] 
**last_name** | **str** |  | [optional] 
**first_name** | **str** |  | [optional] 
**email** | **str** |  | [optional] 
**user** | **str** |  | [optional] 
**task_def** | **int** |  | [optional] 
**phone_number** | **str** |  | [optional] 
**fax_number** | **str** |  | [optional] 
**categories** | **str** |  | [optional] 
**is_scheduling_manpower** | **bool** |  | [optional] 
**enum_value** | **int** |  | [optional] 
**job_title** | **str** |  | [optional] 
**company** | **str** |  | [optional] 

## Example

```python
from gbs4api.models.person_dto import PersonDto

# TODO update the JSON string below
json = "{}"
# create an instance of PersonDto from a JSON string
person_dto_instance = PersonDto.from_json(json)
# print the JSON string representation of the object
print(PersonDto.to_json())

# convert the object into a dict
person_dto_dict = person_dto_instance.to_dict()
# create an instance of PersonDto from a dict
person_dto_from_dict = PersonDto.from_dict(person_dto_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


