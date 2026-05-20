
import gbs3api
from gbs3api.models.customer_dto import CustomerDto
from gbs3api.models.project_data_type import ProjectDataType
from gbs3api.rest import ApiException
from gbs3api.configuration import Configuration
from gbs3api.api_client import ApiClient
from gbs3api.api.masterdata_api import MasterdataApi
from gbs3api.models.person_dto import PersonDto


configuration = Configuration(host="https://alfpwin0044.corp.passivesafety.com/GBS")
configuration.api_key["APIKeyV1"] = "061Fk1h0yUGdOgyKELrneX09EXqC_XN10cEddyuWOyg="

    

def get_test_series(function_number, series_number, include_definition=True):

    with ApiClient(configuration) as api_client:
        api = gbs3api.RequestApi(api_client)
        return api.find_test_series(
            function_number=function_number,
            series_number=series_number,
            include_definition=include_definition
        )

def find_project(function_number, include_definition=True):

    with ApiClient(configuration) as api_client:
        api = gbs3api.RequestApi(api_client)
        return api.find_project(
            function_number=function_number,
            include_definition=include_definition
        )