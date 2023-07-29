from django import template
from django.contrib.auth import get_user_model
from django.template.loader import render_to_string
from django.contrib.auth.decorators import user_passes_test
from django.urls import reverse
from coach_me.profiles.models import BookingUserProfile

register = template.Library()
user_model = get_user_model()


@register.filter
def render_navbar(user):
    user_booking = user_model
    user_booking_profile = BookingUserProfile.objects.filter(pk=user_model.pk).get()
    is_lector = user_booking_profile.is_lector

    if user.is_staff:
        return render_to_string("core/staff_navbar.html")
    elif user.is_authenticated and is_lector:
        return render_to_string("core/lector_navbar.html")
    else:
        return render_to_string("core/default_navbar.html")
