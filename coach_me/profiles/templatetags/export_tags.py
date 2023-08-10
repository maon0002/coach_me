from django import template
from django.urls import reverse

register = template.Library()


@register.simple_tag
def export_csv_link():
    return reverse('export_csv')  # Replace with your app name
