from django.conf import settings
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.urls import path, include
from django.utils.html import strip_tags

from coach_me.bookings.views import IndexView, BookingUpdateView, BookingDeleteView, BookingDetailsView, \
    BookingCreateView

urlpatterns = (
    path('', IndexView.as_view(), name='index'),
    path('booking/add/', BookingCreateView.as_view(), name='add booking'),
    path('booking/<int:pk>/', include([
        path('details/', BookingDetailsView.as_view(), name='details booking'),
        path('edit/', BookingUpdateView.as_view(), name='edit booking'),
        path('delete/', BookingDeleteView.as_view(), name='delete booking'),
    ])),
)


def send_email_after_successful_registration(user):
    html_message = render_to_string(
        'emails/email-registration.html',
        {'profile': user}
    )
    plain_message = strip_tags(html_message)
    send_mail(
        subject='CoachMe Successful registration!',
        message=plain_message,
        html_message=html_message,
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=(user.email, 'manukov.business@gmail.com',),
    )
