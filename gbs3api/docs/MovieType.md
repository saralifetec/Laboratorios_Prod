# MovieType


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**path** | **str** |  | [optional] 
**id_number** | **str** |  | 
**origin** | **str** |  | 
**description** | **str** |  | 
**camera_id_number** | **str** |  | 
**camera_type** | **str** |  | 
**lens_id_number** | **str** |  | 
**lens_type** | **str** |  | 
**focus** | **str** |  | 
**lens_focal_length** | **str** |  | 
**number_of_images** | **str** |  | 
**film_speed** | **str** |  | 
**shutter_time** | **str** |  | 
**aperture** | **str** |  | 
**time_zero** | **str** |  | 
**time_vector_file_name** | **str** |  | 
**reference_system** | **str** |  | 
**location_x** | **str** |  | 
**location_y** | **str** |  | 
**location_z** | **str** |  | 
**theta_x** | **str** |  | 
**theta_y** | **str** |  | 
**theta_z** | **str** |  | 
**width_of_image** | **str** |  | 
**height_of_image** | **str** |  | 
**aspect_ratio_of_pixels** | **str** |  | 
**colour** | **str** |  | 
**name_of_movie_file** | **str** |  | 
**format_of_movie_file** | **str** |  | 
**key_frames** | **str** |  | 
**codec_used** | **str** |  | 
**compression** | **str** |  | 
**distortion_index** | **str** |  | 
**movie_images_corrected** | **str** |  | 
**correction_parameter_file** | **str** |  | 
**image_history_file_name** | **str** |  | 
**source** | **str** |  | [optional] 
**snapshots** | [**List[MovieSnapshotType]**](MovieSnapshotType.md) |  | [optional] 
**additional_group** | [**List[AdditionalGroup]**](AdditionalGroup.md) |  | [optional] 
**element_name** | **str** |  | [optional] 

## Example

```python
from gbs3api.models.movie_type import MovieType

# TODO update the JSON string below
json = "{}"
# create an instance of MovieType from a JSON string
movie_type_instance = MovieType.from_json(json)
# print the JSON string representation of the object
print(MovieType.to_json())

# convert the object into a dict
movie_type_dict = movie_type_instance.to_dict()
# create an instance of MovieType from a dict
movie_type_from_dict = MovieType.from_dict(movie_type_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


