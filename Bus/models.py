from django.db import models
import datetime

class Bus(models.Model):
    bus_no = models.CharField(max_length=20)
    source = models.CharField(max_length=50)
    destination = models.CharField(max_length=50)
    arrival = models.TimeField(default=datetime.time(16, 00))
    fare = models.FloatField(default=0.00)
# Create your models here.

class BookBus(models.Model):
    user = models.CharField(max_length=50,blank=True)
    bus_source = models.CharField(max_length=50)
    bus_destination = models.CharField(max_length=50)
    bus_arrival = models.TimeField()
    seats = models.IntegerField(default=1)
    date = models.DateField(default=datetime.date.today())
    amount = models.FloatField()
    book_id = models.CharField(max_length=100)
    razorpay_payment_id = models.CharField(max_length=100,blank=True)
    paid = models.BooleanField(default=False)
