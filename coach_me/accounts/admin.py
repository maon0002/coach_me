from django.contrib import admin
from coach_me.accounts.models import BookingUser


# Register your models here.
@admin.register(BookingUser)
class BookingUserAdmin(admin.ModelAdmin):
    pass
