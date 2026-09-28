import os
from flask import json
import gbs3api
from gbs3api.api_client import ApiClient
from gbs3api.configuration import Configuration
from gbs3api.api.request_api import RequestApi
from gbs3api.models.test_series_details_dto import (
    TestSeriesDetailsDTO
)
from gbs3api.models.test_step_details_dto import (
    TestStepDetailsDTO
)
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

        print("GBS RESPONSE:")
        pprint(data)

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

        data = json.loads(
            response.data.decode("utf-8")
        )
        
        if not data:
            return None

        return data[0]
