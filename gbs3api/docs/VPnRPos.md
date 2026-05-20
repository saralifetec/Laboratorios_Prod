# VPnRPos


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**path** | **str** |  | [optional] 
**equipment** | [**List[UUCGroup]**](UUCGroup.md) |  | [optional] 
**device** | [**List[UUCGroup]**](UUCGroup.md) |  | [optional] 
**pos** | **str** |  | [optional] 
**element_name** | **str** |  | [optional] 

## Example

```python
from gbs3api.models.vpn_r_pos import VPnRPos

# TODO update the JSON string below
json = "{}"
# create an instance of VPnRPos from a JSON string
vpn_r_pos_instance = VPnRPos.from_json(json)
# print the JSON string representation of the object
print(VPnRPos.to_json())

# convert the object into a dict
vpn_r_pos_dict = vpn_r_pos_instance.to_dict()
# create an instance of VPnRPos from a dict
vpn_r_pos_from_dict = VPnRPos.from_dict(vpn_r_pos_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


