from django.contrib import admin
from coach_me.accounts.models import BookingUser, Company


# Register your models here.
@admin.register(BookingUser)
class BookingUserAdmin(admin.ModelAdmin):
    pass


@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    pass
