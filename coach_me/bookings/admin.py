from django.contrib import admin
from coach_me.bookings.models import Booking, Lector, Training


# Register your models here.
@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    pass

#
# @admin.register(Lector)
# class LectorAdmin(admin.ModelAdmin):
#     filter_horizontal = ('service_integrity',)
#
#
