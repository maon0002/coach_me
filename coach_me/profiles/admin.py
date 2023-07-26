from django.contrib import admin

from coach_me.profiles.models import BookingUserProfile


#
#
# # Register your models here.
#
@admin.register(BookingUserProfile)
class ProfileAdmin(admin.ModelAdmin):
    pass
