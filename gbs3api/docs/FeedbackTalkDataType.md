# FeedbackTalkDataType


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**path** | **str** |  | [optional] 
**operator** | **str** |  | 
**status** | **str** |  | 
**meeting_date** | **datetime** |  | 
**engineer** | **str** |  | [optional] 
**technician** | **str** |  | [optional] 
**mechanic** | **str** |  | [optional] 
**creation_setup_pos** | **str** |  | [optional] 
**creation_setup_neg** | **str** |  | [optional] 
**creation_setup_needed** | **bool** |  | [optional] 
**creation_order_pos** | **str** |  | [optional] 
**creation_order_neg** | **str** |  | [optional] 
**creation_order_needed** | **bool** |  | [optional] 
**creation_logistic_pos** | **str** |  | [optional] 
**creation_logistic_neg** | **str** |  | [optional] 
**creation_logistic_needed** | **bool** |  | [optional] 
**procedure_preparation_pos** | **str** |  | [optional] 
**procedure_preparation_neg** | **str** |  | [optional] 
**procedure_preparation_needed** | **bool** |  | [optional] 
**procedure_procedure_pos** | **str** |  | [optional] 
**procedure_procedure_neg** | **str** |  | [optional] 
**procedure_procedure_needed** | **bool** |  | [optional] 
**procedure_other_pos** | **str** |  | [optional] 
**procedure_other_neg** | **str** |  | [optional] 
**procedure_other_needed** | **bool** |  | [optional] 
**completion_parts_pos** | **str** |  | [optional] 
**completion_parts_neg** | **str** |  | [optional] 
**completion_parts_needed** | **bool** |  | [optional] 
**completion_further_actions** | **str** |  | [optional] 
**optimization_needed** | **bool** |  | [optional] 
**optimization_formulation** | **str** |  | [optional] 
**optimization_improvement** | **str** |  | [optional] 
**element_name** | **str** |  | [optional] 

## Example

```python
from gbs3api.models.feedback_talk_data_type import FeedbackTalkDataType

# TODO update the JSON string below
json = "{}"
# create an instance of FeedbackTalkDataType from a JSON string
feedback_talk_data_type_instance = FeedbackTalkDataType.from_json(json)
# print the JSON string representation of the object
print(FeedbackTalkDataType.to_json())

# convert the object into a dict
feedback_talk_data_type_dict = feedback_talk_data_type_instance.to_dict()
# create an instance of FeedbackTalkDataType from a dict
feedback_talk_data_type_from_dict = FeedbackTalkDataType.from_dict(feedback_talk_data_type_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


