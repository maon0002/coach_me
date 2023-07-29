from django import template
from django.template.loader import render_to_string
from django.contrib.auth.decorators import user_passes_test
from django.urls import reverse

register = template.Library()


@register.filter
def render_navbar(user):
    if user.is_staff:
        return render_to_string("core/staff_navbar.html")
    elif user.is_authenticated and user.is_lector:
        return render_to_string("core/lector_navbar.html")
    else:
        return render_to_string("core/default_navbar.html")
