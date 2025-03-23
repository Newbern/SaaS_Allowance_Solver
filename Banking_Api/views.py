from django.shortcuts import render

# Importing Plaid Banking API
import plaid
from plaid.api import plaid_api
from plaid.models import *
from django.http import JsonResponse

configuration = plaid.Configuration(
    host=plaid.Environment.Sandbox,
    api_key={
        'clientId': '67d9599fb5155d00241374f0',
        'secret': 'b74dd5d810790202194d6d2f316be0',
        'plaidVersion': '2020-09-14'
    }
)

api_client = plaid.ApiClient(configuration)
client = plaid_api.PlaidApi(api_client)

def cuz(request):
    return render(request, 'Banking_Api/Gettinng Link.html', {})

def get_link_token(request):
    link_request = LinkTokenCreateRequest(
        user={"client_user_id": "unique_user_id"},
        client_name="Your App Name",
        products=[Products("transactions")],
        country_codes=[CountryCode('US')],
        language='en'
    )

    response = client.link_token_create(link_request)
    return JsonResponse({'link_token': response['link_token']})