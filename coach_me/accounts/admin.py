from django.contrib import admin
from coach_me.accounts.models import BookingUser
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import Group  # Import Group model



@admin.register(BookingUser)
class BookingUserAdmin(admin.ModelAdmin):
    list_display = ('id', 'email', 'is_staff', 'is_superuser', 'date_joined',)

    list_filter = ('is_staff', 'email',)

    search_fields = ('email',)

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

#
# class CustomUserAdmin(UserAdmin):
#     model = BookingUser
#     list_display = ('email', 'first_name', 'last_name', 'is_staff')
#     list_filter = ('is_staff', 'is_superuser', 'groups')
#
#     fieldsets = (
#         (None, {'fields': ('email', 'password')}),
#         # ('Personal info', {'fields': ('first_name', 'last_name')}),
#         ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
#         ('Important dates', {'fields': ('last_login', 'date_joined')}),
#     )
#
#
# # Register the BookingUser model with the CustomUserAdmin
# admin.site.register(BookingUser, CustomUserAdmin)
#
# # Register the Group model
# admin.site.unregister(Group)
