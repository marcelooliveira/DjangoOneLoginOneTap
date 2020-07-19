from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.views.decorators.http import require_http_methods

from onelogin.saml2.auth import OneLogin_Saml2_Auth
from onelogin.saml2.settings import OneLogin_Saml2_Settings
from onelogin.saml2.utils import OneLogin_Saml2_Utils
from onelogin.api.client import OneLoginClient

import datetime
import mysecrets
import json
import jwt

def index(request):
    if request.session.get('user_data') is not None:
        user_data = json.loads(request.session['user_data'])
        return render(request, 'user-area.html', {'user_data': user_data})
    return render(request, 'index.html', {'one_tap_client_id': mysecrets.ONE_TAP_CLIENT_ID})

def logout(request):
    request.session['user_data'] = None
    return HttpResponseRedirect('/')

@require_http_methods(["POST"])
def one_tap_login(request):
    received_json_data = json.loads(request.body)
    credential = received_json_data['credential']
    decoded = jwt.decode(credential, verify=False)
    user_data = {
        "name": decoded['name'],
        "email": decoded['email'],
        "given_name": decoded['given_name'],
        "family_name": decoded['family_name']
    }
    
    json_user_data = json.dumps(user_data)
    request.session['user_data'] = json_user_data
    # run this in command shell:
    # python manage.py migrate

    client = OneLoginClient(
        mysecrets.ONELOGIN_CLIENT_ID, 
        mysecrets.ONELOGIN_CLIENT_SECRET,
        'us'
    )

    # 1. Make sure the user you want to create does not exist yet
    users = client.get_users({
        "email": decoded["email"]
    })

    # 2. Create the new user (explain the most interesting user parameters)
    if len(users) == 0:
        new_user_params = {
            "email": decoded["email"],
            "firstname": decoded["name"],
            "lastname": decoded["given_name"],
            "username": decoded["family_name"]
        }
        created_user = client.create_user(new_user_params)

        if created_user is not None:

            # 3. Assign the Default role to the user
            roles = client.get_roles({
                "name": "Default"
            })

            if  len(roles) == 1:
                role_ids = [
                    roles[0].id
                ]
                client.assign_role_to_user(created_user.id, role_ids)

            # 4. Set the user state
            USER_STATE_APPROVED = 1
            client.set_state_to_user(created_user.id, USER_STATE_APPROVED)

    return HttpResponse(json_user_data, content_type="application/json")