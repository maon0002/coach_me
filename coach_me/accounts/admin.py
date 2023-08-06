from django.contrib import admin
from coach_me.accounts.models import BookingUser


# Register your models here.
@admin.register(BookingUser)
class BookingUserAdmin(admin.ModelAdmin):
    list_display = ('email', 'is_staff', 'is_superuser', 'date_joined')

    # Variable 2: list_filter
    list_filter = ('is_staff', 'email',)

    # Variable 3: search_fields
    search_fields = ('email',)

    # Variable 4: fieldsets
    fieldsets = (
        ('User Details', {
            'fields': ('email', 'password')
        }),
        ('Permissions', {
            'fields': (
                # 'is_active',
                'is_staff',
                'is_superuser',
                'groups',
                'user_permissions'
            ),
        }),
        # ('Important dates', {
        #     'fields': ('last_login', 'date_joined'),
        # }),
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
