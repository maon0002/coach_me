from django.apps import AppConfig


class BookingConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'coach_me.bookings'

    def ready(self):
        # Import and register your custom template tags module
        import coach_me.bookings.templatetags.navbar_tags
