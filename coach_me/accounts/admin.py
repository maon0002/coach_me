from django.contrib import admin
from coach_me.accounts.models import BookingUser


@admin.register(BookingUser)
class BookingUserAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'email',
        'is_staff',
        'is_superuser',
        'date_joined',
        'c_labels',
    )

    list_filter = (
        'is_staff',
        'email',
        'c_labels',
    )

    search_fields = (
        'email',
    )

    fieldsets = (
        ('User Details', {
            'fields': ('email', 'password')
        }),
        ('Permissions', {
            'fields': (
                'is_staff',
                'is_superuser',
                'c_labels',
                'groups',
                'user_permissions'
            ),
        }),
    )

    ordering = ['-date_joined']

    list_per_page = 20

    list_max_show_all = 1000

    save_on_top = True

    show_full_result_count = True

    # Property for user's full name (email)
    def full_name(self, obj):
        return obj.email

    full_name.short_description = 'Full Name'
