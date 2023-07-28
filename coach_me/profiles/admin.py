from django.contrib import admin

from coach_me.profiles.models import BookingUserProfile, Company


#
#
# # Register your models here.
#
@admin.register(BookingUserProfile)
class ProfileAdmin(admin.ModelAdmin):
    pass


@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    pass
