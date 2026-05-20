from api_client import Configuration, ApiClient
from api_client.api.master_data_controller_api import MasterDataControllerApi
from api_client.rest import ApiException
from pprint import pprint

configuration = Configuration(
    host="https://alfpwin0044.corp.passivesafety.com/GBS/webservice"
)

configuration.access_token = "061Fk1h0yUGdOgyKELrneX09EXqC_XN10cEddyuWOyg="

with ApiClient(configuration) as api_client:
    api_instance = MasterDataControllerApi(api_client)

    try:
        api_response = api_instance.find_customers()
        
        customers = api_response
        for c in customers:
            print(c.id, c.name)


    except ApiException as e:
        print("Erro ao chamar a API")
        print(f"Status: {e.status}")
        print(f"Body: {e.body}")
