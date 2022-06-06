from django.db import models

class City(models.Model):
    city = models.CharField(max_length=50, default="")

    @staticmethod
    def get_all_cities():
        return City.objects.all()
    
    @staticmethod
    def get_weather_data(city):
        return City.objects.get(city = city)

    @staticmethod
    def add_city(city):
        c = City(city = city)
        c.save()

    @staticmethod
    def already_present(city):
        try:
            c = City.objects.get(city = city)
        except City.DoesNotExist:
            c = False
        return c
    
    @staticmethod
    def delete_city(city):
        City.objects.get(city = city).delete()
