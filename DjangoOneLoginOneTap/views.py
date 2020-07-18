from django.http import HttpResponse
from django.shortcuts import render
from django.views.decorators.http import require_http_methods
import datetime
import mysecrets

def index(request):
    return render(request, 'index.html', {'one_tap_client_id': mysecrets.ONE_TAP_CLIENT_ID})


@require_http_methods(["POST"])
def one_tap_login(request):
    return HttpResponse()