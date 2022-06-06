from django.shortcuts import render, redirect
from django.views import View
from weather.models.city import City
from django.contrib import messages
from django.http import HttpResponse, HttpResponseRedirect
import json, math
import requests

class Index(View):
    def post(self, request):
        city = request.POST.get("city")
        print(city)
        trash = request.POST.get("trash")
        
        status = False
        if city:
            city = city.upper()
            status = True
            existing_city = City.already_present(city)
            if not existing_city:
                new_city_data = self.get_weather_data(city)
                if(new_city_data['cod'] == 200): 
                    City.add_city(city)
                else:
                    status = False
                    message = 'This City does not exist'
                    message_class = "error"
            else:
                status = False
                message = 'This City already exists'
                message_class = "error"
                
            if (status):
                message = f'{city} city added succesfully'
                message_class = "success"
        
        if (trash):
            City.delete_city(trash)
            message = f'{trash} city deleted succesfully'
            message_class = "success"

        weather_cities = self.weather_for_all()
        return render(request, "index.html", {"weather_data":weather_cities, "message":message, "message_class":message_class})
    

    def get(self, request):
        weather_cities = self.weather_for_all()
        return render(request, "index.html", {"weather_data":weather_cities})
    

    def get_weather_data(self, city):
        url = f'https://api.openweathermap.org/data/2.5/weather?q={city}&appid=9a2401199e06b1cf8ad42cd31fe45f8b'
        r = requests.get(url).json()
        return r
    

    def weather_for_all(self):
        cities = City.get_all_cities()
        weather_cities = []
        for c in cities:
            r = self.get_weather_data(c.city)
            weather ={
                    "city": c.city,

                    "temperature": math.ceil(r["main"]["temp"]),
                    "min_temperature": r["main"]["temp_min"],
                    "max_temperature": r["main"]["temp_max"],
                    "feels": r["main"]["feels_like"],

                    "description": r["weather"][0]["description"],
                    "icon": r["weather"][0]["icon"],

                    "wind": r["wind"]["speed"],
                    "humidity": r["main"]["humidity"],
                    "visibility": r["visibility"]
            }
            weather_cities.insert(0, weather)
        return weather_cities
