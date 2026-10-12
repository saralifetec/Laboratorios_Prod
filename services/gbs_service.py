import os
from flask import json
import gbs3api
from gbs3api.api_client import ApiClient
from gbs3api.configuration import Configuration
from gbs3api.api.request_api import RequestApi
from gbs3api.models.test_step_details_dto import TestStepDetailsDTO
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

        params = api._find_test_step_details_serialize(
            id=test_series_id,
            _request_auth=None,
            _content_type=None,
            _headers=None,
            _host_index=0
        )

        response = api_client.call_api(*params)

        response.read()

        raw = response.data.decode("utf-8")

        print("RAW RESPONSE:")
        print(raw)

        return json.loads(raw)

        


def get_person_gbs(username):

    with gbs3api.ApiClient(configuration) as api_client:

        api = gbs3api.MasterdataApi( api_client )

        pessoas = api.get_persons1( username=username )

        if not pessoas:
            return None

        pessoa = pessoas[0]

        return {
            'username': pessoa.user,
            'nome': f'{pessoa.first_name} {pessoa.last_name}',
            'email': pessoa.email
        }

def get_jwt_info():

    with gbs3api.ApiClient( configuration ) as api_client:

        api = gbs3api.AuthenticationApi(
            api_client
        )

        return api.get_jwt_info()
