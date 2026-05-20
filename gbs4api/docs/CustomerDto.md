# CustomerDto


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**id** | **int** |  | [optional] 
**name** | **str** |  | [optional] 
**description** | **str** |  | [optional] 
**persons** | **List[int]** |  | [optional] 

## Example

```python
from gbs4api.models.customer_dto import CustomerDto

# TODO update the JSON string below
json = "{}"
# create an instance of CustomerDto from a JSON string
customer_dto_instance = CustomerDto.from_json(json)
# print the JSON string representation of the object
print(CustomerDto.to_json())

# convert the object into a dict
customer_dto_dict = customer_dto_instance.to_dict()
# create an instance of CustomerDto from a dict
customer_dto_from_dict = CustomerDto.from_dict(customer_dto_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


