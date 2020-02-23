from django.shortcuts import render
from django.http import JsonResponse
import requests
import os
import local_settings

def home(request):
    ip = requests.get("https://api.ipify.org/").text
    location = requests.get("http://ip-api.com/json/{0}".format(ip))
    location = location.json()
    city = location.get("city")
    country_code = location.get("countryCode")
    token = local_settings.OPEN_WEATHER_TOKEN
    url = "https://api.openweathermap.org/data/2.5/weather?q={0},{1}&units=metric&appid={2}".format(city, country_code, token)
    weather_data = requests.get(url)
    weather_data = weather_data.json()
    temp = str(weather_data['main']['temp'],)
    temp= int(temp[0:2])
    mintemp = str(weather_data['main']['temp_min'])
    mintemp = int(mintemp[0:2])
    maxtemp = str(weather_data['main']['temp_max'])
    maxtemp = int(maxtemp[0:2])
    feelslike = str(weather_data['main']['feels_like'])
    feelslike = int(feelslike[0:2])

    weather = {
        'city' : city,
        'temperature' : temp,
        'feelslike' : feelslike,
        'tempmin' : mintemp,
        'tempmax' : maxtemp,
        'humidity' : weather_data['main']['humidity'],
        'main' : weather_data['weather'][0]['main'],
        'description' : weather_data['weather'][0]['description'],
        'icon' : weather_data['weather'][0]['icon']
    }





    color = ''
    timezone = requests.get("https://api.ipgeolocation.io/timezone?apiKey=1fc41273a3ef468790a11c6d410bbe84&ip={0}".format(ip))
    timezone = timezone.json()
    time = str(timezone['time_24'])
    short_time = int(time[0:2])
    if (short_time >= 5) and (short_time <= 6):
        color = '#5B7A93'
    elif (short_time >= 7) and (short_time <= 17):
        color = '#0A80DF'
    elif (short_time >= 18) and (short_time <= 19):
        color = '#5B7A93'
    else:
        color = '#3D3D40'


    weather_id = weather_data['weather'][0]['id']


    image_id = ""
    if (weather_id>= 200) and (weather_id <= 232):
        image_id = "THUNDERSTORM"
    if (weather_id>= 300) and (weather_id <= 321):
        image_id = "DRIZZLE"
    if (weather_id>= 500) and (weather_id <= 532):
        image_id = "RAIN"
    if (weather_id>= 600) and (weather_id <= 622):
        image_id = "SNOW"
    if (weather_id>= 701) and (weather_id <= 781):
        image_id = "ATMOSPHERE"
    if (weather_id == 800) and (short_time <= 5) and (short_time >= 18):
        image_id = "CLEAR_NIGHT"
    if (weather_id == 800) and (short_time >= 6) and (short_time <= 17):
        image_id = "CLEAR_DAY"
    if (weather_id >= 801) and (weather_id <= 805) and (short_time <= 5) or (short_time >= 18):
        image_id = "CLOUDS_NIGHT"
    if (weather_id >= 801) and (weather_id <= 805) and (short_time >= 6) and (short_time <= 17):
        image_id = "CLOUDS_DAY"










    context = {'weather' : weather, 'color':color, 'image_id':image_id,}


    return render(request, 'weather/index.html', context)
