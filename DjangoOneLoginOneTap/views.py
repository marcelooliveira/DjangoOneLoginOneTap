from django.http import HttpResponse
from django.shortcuts import render
from django.views.decorators.http import require_http_methods
import datetime
import mysecrets
import json
import jwt

def index(request):
    json_user_data = request.session['user_data']
    if json_user_data is not None:
        user_data = json.loads(json_user_data)
        return render(request, 'user-area.html', {'user_data': user_data})
    return render(request, 'index.html', {'one_tap_client_id': mysecrets.ONE_TAP_CLIENT_ID})

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

    return HttpResponse(json_user_data, content_type="application/json")