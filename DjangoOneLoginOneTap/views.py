from django.http import HttpResponse
from django.shortcuts import render
import datetime
import mysecrets

def index(request):
    return render(request, 'index.html', {'one_tap_client_id': mysecrets.ONE_TAP_CLIENT_ID})

def one_tap_login(request):
    return HttpResponse()