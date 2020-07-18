from django.http import HttpResponse
from django.shortcuts import render
import datetime

def index(request):
    return render(request, 'index.html')