from django.contrib import admin
from coach_me.lectors.models import Lector


@admin.register(Lector)
class LectorAdmin(admin.ModelAdmin):
    filter_horizontal = ('service_integrity',)

    list_display = ('full_name', 'email', 'phone', )

    list_filter = ('inserted_on', 'updated_on')

    search_fields = ('first_name', 'last_name', 'email', 'phone')

    fieldsets = (
        ('Lector Information', {
            'fields': (
            'user', 'first_name', 'last_name', 'phone', 'email', 'lector_image', 'service_integrity', 'biography',
            'slug')
        }),
        # ('Date Information', {
        #     'fields': ('inserted_on', 'updated_on')
        # }),
    )

    ordering = ['last_name', 'first_name']

    list_per_page = 20

    list_max_show_all = 1000

    save_on_top = True

    show_full_result_count = True

    # Property for full name
    def full_name(self, obj):
        return obj.full_name

    full_name.short_description = 'Full Name'

    # Property for service integrity (to display in list view)
    def service_integrity_list(self, obj):
        return ", ".join([service.service_name for service in obj.service_integrity.all()])

    service_integrity_list.short_description = 'Service Integrity'

    # Property for biography (to display in list view)
    def biography_summary(self, obj):
        return obj.biography[:50]

    biography_summary.short_description = 'Biography Summary'
