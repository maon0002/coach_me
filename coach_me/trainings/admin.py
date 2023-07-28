from django.contrib import admin
from coach_me.trainings.models import Training


@admin.register(Training)
class TrainingAdmin(admin.ModelAdmin):
    pass
