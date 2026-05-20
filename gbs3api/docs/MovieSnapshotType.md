# MovieSnapshotType


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**path** | **str** |  | [optional] 
**number_of_snapshots** | **int** |  | [optional] 
**snapshot** | [**List[ImageType]**](ImageType.md) |  | [optional] 
**additional_group** | [**List[AdditionalGroup]**](AdditionalGroup.md) |  | [optional] 
**element_name** | **str** |  | [optional] 

## Example

```python
from gbs3api.models.movie_snapshot_type import MovieSnapshotType

# TODO update the JSON string below
json = "{}"
# create an instance of MovieSnapshotType from a JSON string
movie_snapshot_type_instance = MovieSnapshotType.from_json(json)
# print the JSON string representation of the object
print(MovieSnapshotType.to_json())

# convert the object into a dict
movie_snapshot_type_dict = movie_snapshot_type_instance.to_dict()
# create an instance of MovieSnapshotType from a dict
movie_snapshot_type_from_dict = MovieSnapshotType.from_dict(movie_snapshot_type_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


