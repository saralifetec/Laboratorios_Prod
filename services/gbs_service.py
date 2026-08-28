import os

from flask import json
import gbs3api
from gbs3api.configuration import Configuration
from gbs3api.models.test_series_details_dto import TestSeriesDetailsDTO
from gbs3api.models.test_step_details_dto import TestStepDetailsDTO
from gbs3api.rest import ApiException
from pprint import pprint


configuration = Configuration(host="https://alfpwin0044.corp.passivesafety.com/GBS")
configuration.api_key["APIKeyV1"] = "ZPuN1kbUqRzBwpUjgyGI2YnEog_OX5RKd3MZKSJfDY0="
configuration.debug = True


def find_test_series_details(full_series_number):

    with gbs3api.ApiClient(configuration) as api_client:

        api = gbs3api.RequestApi(api_client)

        response = api.find_test_series_details_without_preload_content(
            full_series_number=full_series_number
        )

        data = json.loads(
            response.data.decode("utf-8")
        )

        if not data:
            return None

        return data[0]

def find_test_step_details(test_series_id):

    with gbs3api.ApiClient(configuration) as api_client:

        api = gbs3api.RequestApi(api_client)

        print(
            "TEST SERIES ID:",
            test_series_id
        )

        response = api.find_test_step_details(
            test_series_id
        )

        return response

    
#teste - apagar
def find_project(function_number):

    with gbs3api.ApiClient(configuration) as api_client:

        api = gbs3api.RequestApi(api_client)

        print(
            "FUNCTION NUMBER:",
            function_number
        )

        try:

            response = api.find_project(
                function_number,
                include_definition=False
            )



            print("TIPO:")
            print(type(response))

            return response

        except Exception as e:

            print("ERRO:")
            print(type(e))
            print(e)

            raise