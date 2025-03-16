from django.shortcuts import render

# Create your views here.
def test(request):
    return render(request, 'Banking_Api/test.html', {})


from plaid.model.link_token_create_request import LinkTokenCreateRequest
from plaid.model.link_token_create_request_user import LinkTokenCreateRequestUser
from plaid.model.products import Products
from plaid.model.country_code import CountryCode

def create_link_token():
    # Get the client_user_id by searching for the current user
    user = '67d9599fb5155d00241374f0'
    client_user_id = '67d9599fb5155d00241374f0'

    # Create a link_token for the given user
    request = LinkTokenCreateRequest(
            products=[Products("auth")],
            client_name="Plaid Test App",
            country_codes=[CountryCode('US')],
            redirect_uri='https://domainname.com/oauth-page.html',
            language='en',
            webhook='https://webhook.example.com',
            user=LinkTokenCreateRequestUser(
                client_user_id=client_user_id
            )
        )
    response = client.link_token_create(request)

    # Send the data to the client
    return jsonify(response.to_dict())