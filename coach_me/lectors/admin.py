from django.contrib import admin
from coach_me.lectors.models import Lector


@admin.register(Lector)
class LectorAdmin(admin.ModelAdmin):
    filter_horizontal = ('service_integrity',)
