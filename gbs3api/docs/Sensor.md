# Sensor


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**path** | **str** |  | [optional] 
**cal_version** | **int** |  | [optional] 
**scaling_method** | **str** |  | [optional] 
**sensitivity** | **float** |  | [optional] 
**engineering_unit** | **str** |  | [optional] 
**sensitivity2** | **float** |  | [optional] 
**sensitivity3** | **float** |  | [optional] 
**sensitivity4** | **float** |  | [optional] 
**sensitivity5** | **float** |  | [optional] 
**sensitivity_voltage** | **float** |  | [optional] 
**linearity_deviation** | **float** |  | [optional] 
**standard_deviation** | **float** |  | [optional] 
**cal_date** | **datetime** |  | [optional] 
**cal_person** | **str** |  | [optional] 
**cal_laboratory** | **str** |  | [optional] 
**cal_instruction** | **str** |  | [optional] 
**cal_remark** | **str** |  | [optional] 
**cal_protocol** | **str** |  | [optional] 
**reference_calibration** | **bool** |  | [optional] 
**hysteresis_deviation** | **float** |  | [optional] 
**additional_group** | [**List[AdditionalGroup]**](AdditionalGroup.md) |  | [optional] 
**name** | **str** |  | 
**uuid** | **str** |  | 
**enabled** | **bool** |  | [optional] 
**readout_enabled** | **bool** |  | [optional] 
**conversion_enabled** | **bool** |  | [optional] 
**teds_type** | **str** |  | [optional] 
**location_code** | **str** |  | [optional] 
**location_longname** | **str** |  | [optional] 
**company_code** | **str** |  | [optional] 
**company_longname** | **str** |  | [optional] 
**supplier** | **str** |  | [optional] 
**model** | **str** |  | [optional] 
**technology** | **str** |  | [optional] 
**excitation_voltage_min** | **float** |  | [optional] 
**excitation_voltage_max** | **float** |  | [optional] 
**electrical_method** | **str** |  | [optional] 
**physical_dimension** | **str** |  | [optional] 
**physical_unit** | **str** |  | [optional] 
**axis_direction** | **str** |  | [optional] 
**min_range** | **float** |  | [optional] 
**max_range** | **float** |  | [optional] 
**max_sensitivity_deviation** | **float** |  | [optional] 
**max_linearity_deviation** | **float** |  | [optional] 
**max_standard_deviation** | **float** |  | [optional] 
**max_hysteresis_deviation** | **float** |  | [optional] 
**serial_number** | **str** |  | [optional] 
**usable** | **bool** |  | [optional] 
**status** | **str** |  | [optional] 
**cal_period** | **int** |  | [optional] 
**shunt_check_pos** | **bool** |  | [optional] 
**shunt_gain_pos** | **float** |  | [optional] 
**shunt_value_pos** | **float** |  | [optional] 
**shunt_tol_relative_pos** | **float** |  | [optional] 
**shunt_check_neg** | **bool** |  | [optional] 
**shunt_gain_neg** | **float** |  | [optional] 
**shunt_value_neg** | **float** |  | [optional] 
**shunt_tol_relative_neg** | **float** |  | [optional] 
**shunt_resistance** | **float** |  | [optional] 
**bridge_resistor_pinp_pexc** | **float** |  | [optional] 
**bridge_resistor_pinp_nexc** | **float** |  | [optional] 
**bridge_resistor_ninp_pexc** | **float** |  | [optional] 
**bridge_resistor_ninp_nexc** | **float** |  | [optional] 
**offset** | **float** |  | [optional] 
**offset_tol** | **float** |  | [optional] 
**offset_check** | **bool** |  | [optional] 
**electrical_polarity** | **str** |  | [optional] 
**connector_pin** | [**List[Pin]**](Pin.md) |  | [optional] 
**connector_type** | **str** |  | [optional] 
**connector_id** | **str** |  | [optional] 
**cal_history** | [**List[CalHistoryEntry]**](CalHistoryEntry.md) |  | [optional] 
**calibration_category** | **str** |  | [optional] 
**source_calibration** | [**CalHistoryEntry**](CalHistoryEntry.md) |  | [optional] 
**current_calibration** | [**CalHistoryEntry**](CalHistoryEntry.md) |  | [optional] 
**maintenance_category** | **str** |  | [optional] 
**maintenance_date** | **datetime** |  | [optional] 
**maintenance_period** | **int** |  | [optional] 
**next_maintenance_date** | **datetime** |  | [optional] 
**current_maintenance** | [**CalHistoryEntry**](CalHistoryEntry.md) |  | [optional] 
**maintenances** | [**List[CalHistoryEntry]**](CalHistoryEntry.md) |  | [optional] 
**verification_category** | **str** |  | [optional] 
**verification_date** | **datetime** |  | [optional] 
**verification_period** | **int** |  | [optional] 
**next_verification_date** | **datetime** |  | [optional] 
**current_verification** | [**CalHistoryEntry**](CalHistoryEntry.md) |  | [optional] 
**verifications** | [**List[CalHistoryEntry]**](CalHistoryEntry.md) |  | [optional] 
**device_channel_name** | **str** |  | [optional] 
**mounting_polarity** | **str** |  | [optional] 
**remark** | **str** |  | [optional] 
**preferred_range** | **float** |  | [optional] 
**sample_frequency** | **float** |  | [optional] 
**excitation_voltage** | **float** |  | [optional] 
**offset_compensation** | **bool** |  | [optional] 
**const_in_read_only** | **bool** |  | [optional] 
**const_in_value** | **float** |  | [optional] 
**firing_mode** | **str** |  | [optional] 
**firing_delay** | **float** |  | [optional] 
**firing_duration** | **int** |  | [optional] 
**firing_voltage_limit** | **int** |  | [optional] 
**firing_current_limit** | **int** |  | [optional] 
**resource_type_scheduling** | **str** |  | [optional] 
**resource_type_scheduling_id** | **str** |  | [optional] 
**sensor_status** | **str** |  | [optional] 
**last_status_change** | **datetime** |  | [optional] 
**responsible_person** | **str** |  | [optional] 
**inventory_number** | **str** |  | [optional] 
**cost_center** | **str** |  | [optional] 
**purchase_date** | **datetime** |  | [optional] 
**location** | **str** |  | [optional] 
**element_name** | **str** |  | [optional] 
**swoffset_compensation** | **bool** |  | [optional] 
**idmodule_string** | **str** |  | [optional] 
**swoffset_compensation_type** | **str** |  | [optional] 
**idmodule_type** | **str** |  | [optional] 
**swoffset_calculation_start_sec** | **float** |  | [optional] 
**swoffset_calculation_end_sec** | **float** |  | [optional] 
**swoffset_fix_value** | **float** |  | [optional] 
**swfilter_class_type** | **str** |  | [optional] 
**swfilter_ad_hoc_frequency** | **float** |  | [optional] 

## Example

```python
from gbs3api.models.sensor import Sensor

# TODO update the JSON string below
json = "{}"
# create an instance of Sensor from a JSON string
sensor_instance = Sensor.from_json(json)
# print the JSON string representation of the object
print(Sensor.to_json())

# convert the object into a dict
sensor_dict = sensor_instance.to_dict()
# create an instance of Sensor from a dict
sensor_from_dict = Sensor.from_dict(sensor_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


