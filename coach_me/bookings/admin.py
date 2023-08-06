from django.contrib import admin
from coach_me.bookings.models import Booking, Lector, Training


# Register your models here.
@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'employee',
        'phone',
        'booking_type',
        'lector')

    list_filter = (
        'employee', 'booking_type', 'lector',
        # 'first_name', 'last_name',
    )

    fieldsets = (
        ('Booking Information', {
            'fields': (
                'start_date',
                'start_time',
                'booking_type',
                'training_mode',
                'lector',
                'notes',
                'certificate_code',

            )
        }),
        ('Employee Information', {
            'fields': (
                'first_name',
                'last_name',
                'phone',
                'employee',
                'private_email',
                'preferred_platforms',
            )
        }),
        ('Company Information', {
            'fields': (
                'company_name',
                'corporate_email',
            )
        }),
        ('Payment Information', {
            'fields': (
                'price',
                'paid',
                'amount_paid_online',
            )
        }),
    )

    ordering = ['id', 'last_name', 'first_name', 'booking_type', 'lector']

    list_per_page = 20

    list_max_show_all = 1000

    save_on_top = True

    show_full_result_count = True
