from django.contrib import admin
from coach_me.trainings.models import Training


@admin.register(Training)
class TrainingAdmin(admin.ModelAdmin):
    list_display = ('id', 'service_name', 'service_description', 'inserted_on', 'updated_on')

    list_filter = ('service_name', 'inserted_on', 'updated_on')

    search_fields = ('service_name', 'service_description')

    fieldsets = (
        ('Service Information', {
            'fields': ('service_name', 'service_description', 'service_image', 'slug')
        }),
        # ('Date Information', {
        #     'fields': ('inserted_on', 'updated_on')
        # }),
    )

    ordering = ['-inserted_on']

    list_per_page = 20

    list_max_show_all = 1000

    save_on_top = True

    show_full_result_count = True

    # Property for service name and description
    def service_name_and_description(self, obj):
        return f'{obj.service_name} - {obj.service_description[:50]}'

    service_name_and_description.short_description = 'Service Name and Description'

    list_display_links = (
        'id',
    )

    list_editable = (
        'service_name',
    )
