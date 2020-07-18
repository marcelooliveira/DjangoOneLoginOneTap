from django.http import HttpResponse
from django.shortcuts import render
from django.views.decorators.http import require_http_methods
import datetime
import mysecrets
import json
import jwt

def index(request):
    return render(request, 'index.html', {'one_tap_client_id': mysecrets.ONE_TAP_CLIENT_ID})

@require_http_methods(["POST"])
def one_tap_login(request):
    received_json_data = json.loads(request.body)
    credential = received_json_data['credential']
    decoded = jwt.decode(credential, verify=False)  
    return HttpResponse(content=decoded['name'])