# GbsInstanceDto


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**host** | **str** |  | [optional] 
**version** | **str** |  | [optional] 
**currently_logged_user** | **str** |  | [optional] 

## Example

```python
from gbs3api.models.gbs_instance_dto import GbsInstanceDto

# TODO update the JSON string below
json = "{}"
# create an instance of GbsInstanceDto from a JSON string
gbs_instance_dto_instance = GbsInstanceDto.from_json(json)
# print the JSON string representation of the object
print(GbsInstanceDto.to_json())

# convert the object into a dict
gbs_instance_dto_dict = gbs_instance_dto_instance.to_dict()
# create an instance of GbsInstanceDto from a dict
gbs_instance_dto_from_dict = GbsInstanceDto.from_dict(gbs_instance_dto_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


