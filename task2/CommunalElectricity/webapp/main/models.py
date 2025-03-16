
from django.db import models
from django.utils import timezone

class User(models.Model):
    name = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    email = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return f"{self.name} ({self.email})"


class Meter(models.Model):
    meter_number = models.BigIntegerField(unique=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"Лічильник №{self.meter_number}"


class Reading(models.Model):
    meter = models.ForeignKey(Meter, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    day_kwh = models.IntegerField()
    night_kwh = models.IntegerField()

    def __str__(self):
        local_date = timezone.localtime(self.date)
        return f"Показник лічильника №{self.meter.meter_number} ({local_date.strftime('%d-%m-%Y %H:%M:%S')}) - Денний показник: {self.day_kwh} кВт⋅год, Нічний показник: {self.night_kwh} кВт⋅год"


class Bill(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    meter = models.ForeignKey(Meter, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    day_usage = models.FloatField()
    night_usage = models.FloatField()
    total_price = models.FloatField()

    def __str__(self):
        local_date = timezone.localtime(self.date)
        return f"Рахунок за {local_date.strftime('%d-%m-%Y %H:%M:%S')} - {self.user.name} - {self.total_price} грн"


