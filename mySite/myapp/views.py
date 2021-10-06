from django.shortcuts import render
from django.http import HttpResponse
import requests
# from .models import Book
# Create your views here.
def index(request):
    #   My Own API Key you may use yours if you'd like
    apikey='215E7ED2-8B7D-2842-A5B0-B6F438ECB5998AB6FBC2-59BA-41CC-B54C-B96011624A9B'
    url=f'https://api.guildwars2.com/v2/characters'
    response=requests.get(url,data={'access_token':apikey})
    return HttpResponse(response)
    