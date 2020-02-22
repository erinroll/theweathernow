from django.shortcuts import render
from django.http import JsonResponse
import requests


def home(request):
    return render(request, 'weather/index.html')

def get_location_from_ip (ip_address):
    response = requests.get("http://ip-api.com/json/{0}".format(ip_address))
    return response.json()

def get_weather_from_ip(request):
    ip_address = request.GET.get("ip")
    location = get_location_from_ip(ip_address)
    city = location.get("city")
    country_code = location.get("countryCode")
    s = "You're in {0}, {1}".format(city,country_code)
    data = {"weather_data": s}
    return JsonResponse(data)
