# MovieInformationType


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**path** | **str** |  | [optional] 
**number_of_movies** | **int** |  | [optional] 
**source** | **str** |  | [optional] 
**movie** | [**List[MovieType]**](MovieType.md) |  | [optional] 
**additional_group** | [**List[AdditionalGroup]**](AdditionalGroup.md) |  | [optional] 
**element_name** | **str** |  | [optional] 

## Example

```python
from gbs3api.models.movie_information_type import MovieInformationType

# TODO update the JSON string below
json = "{}"
# create an instance of MovieInformationType from a JSON string
movie_information_type_instance = MovieInformationType.from_json(json)
# print the JSON string representation of the object
print(MovieInformationType.to_json())

# convert the object into a dict
movie_information_type_dict = movie_information_type_instance.to_dict()
# create an instance of MovieInformationType from a dict
movie_information_type_from_dict = MovieInformationType.from_dict(movie_information_type_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


