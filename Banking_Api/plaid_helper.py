# plaid_helper.py
from plaid.api import plaid_api
from plaid.model import *
from plaid.configuration import Configuration
from plaid.api_client import ApiClient
from django.conf import settings

def get_plaid_client():
    # Correctly set the environment
    if settings.PLAID_ENV == 'sandbox':
        host = 'https://sandbox.plaid.com'
    elif settings.PLAID_ENV == 'development':
        host = 'https://development.plaid.com'
    else:
        host = 'https://production.plaid.com'

    # Configure Plaid API client
    config = Configuration(
        host=host,
        api_key={
            'clientId': settings.PLAID_CLIENT_ID,
            'secret': settings.PLAID_SECRET
        }
    )
    api_client = ApiClient(config)
    return plaid_api.PlaidApi(api_client)
