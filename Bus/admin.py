from django.contrib import admin
from Bus.models import Bus
from Bus.models import BookBus

class BusAdmin(admin.ModelAdmin):
    list_display=("bus_no","source","destination","arrival","fare")

admin.site.register(Bus,BusAdmin)

class BookBusAdmin(admin.ModelAdmin):
    list_display=("user","bus_source","bus_destination","bus_arrival","amount","book_id","razorpay_payment_id","paid")

admin.site.register(BookBus,BookBusAdmin)

# Register your models here.
