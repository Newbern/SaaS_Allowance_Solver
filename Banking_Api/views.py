from django.shortcuts import render, redirect

# Importing Plaid Banking API
import plaid
from plaid.api import plaid_api
from plaid.models import *
from django.http import JsonResponse
import json
from django.views.decorators.csrf import csrf_exempt
from Banking_Api.models import *

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
    transactions(request)
    return render(request, 'Banking_Api/Gettinng Link.html', {})


def get_link_token(request):
    link_request = LinkTokenCreateRequest(
        user={"client_user_id": "67d9599fb5155d00241374f0"},
        client_name="Allowance Solver",
        products=[Products("transactions")],
        country_codes=[CountryCode('US')],
        language='en'
    )

    response = client.link_token_create(link_request)
    return JsonResponse({'link_token': response['link_token']})


@csrf_exempt
def exchange_public_token(request):
    data = json.loads(request.body)
    public_token = data.get('public_token')

    # Exchange public_token for access_token
    exchange_request = ItemPublicTokenExchangeRequest(public_token=public_token)
    exchange_response = client.item_public_token_exchange(exchange_request)

    # Save user’s access_token and item_id
    Account.objects.create(user=request.user, access_token=exchange_response.access_token, item_id=exchange_response.item_id).save()

    return redirect('home')

def transactions(request):
    user = Account.objects.filter(user=request.user).first()
    from datetime import timedelta
    import datetime

    # Define Request
    request = TransactionsGetRequest(
        access_token=user.access_token,
        start_date=datetime.date.today(),
        end_date=datetime.date.today() + datetime.timedelta(days=1),
        options=TransactionsGetRequestOptions(
            count=500,  # Max per request
            offset=0,
        ),
    )

    # Paginate through results
    transactions = []
    has_more = True
    while has_more:
        response = client.transactions_get(request)
        transactions.extend(response["transactions"])
        has_more = response["total_transactions"] > len(transactions)
        request.options.offset += len(response["transactions"])

    print(transactions)

