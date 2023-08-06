from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from coach_me.bookings.models import Booking
from coach_me.lectors.models import Lector
from coach_me.profiles.models import BookingUserProfile, Company

UserModel = get_user_model()


def send_email_to_user_after_booking_creation(booking):
    # Get the user associated with the booking
    user = booking.employee

    # Get the booking user profile associated with the user
    booking_user_profile = BookingUserProfile.objects.get(pk=user.pk)

    # Get the lector associated with the booking
    lector = booking.lector

    # Get the training associated with the booking
    training = booking.booking_type

    html_message = render_to_string(
        'emails/email-create-booking-user.html',
        {
            'profile': booking_user_profile,
            'booking': booking,
            'lector': lector,
            'training': training,

        }
    )
    plain_message = strip_tags(html_message)
    send_mail(
        subject='CoachMe Successful booking creation!',
        message=plain_message,
        html_message=html_message,
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=(
            user.email,
            'manukov.business@gmail.com',
        ),
    )


def send_email_to_lector_after_booking_creation(booking):
    # Get the user associated with the booking
    user = booking.employee

    # Get the booking user profile associated with the user
    booking_user_profile = BookingUserProfile.objects.get(pk=user.pk)

    # Get the lector associated with the booking
    lector = booking.lector

    # Get the training associated with the booking
    training = booking.booking_type

    # Get the company associated with the employee
    company = Company.objects.filter(company_domain__iendswith=user.email.split('@')[1]).get()

    html_message = render_to_string(
        'emails/email-create-booking-lector.html',
        {
            'profile': booking_user_profile,
            'booking': booking,
            'lector': lector,
            'training': training,
            'company': company,
        }
    )
    plain_message = strip_tags(html_message)
    send_mail(
        subject='CoachMe Successful booking with you as a Lector!',
        message=plain_message,
        html_message=html_message,
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=(
            'manukov.business@gmail.com',
            lector.email,
        ),
    )


def send_email_to_user_after_booking_update(booking):
    # Get the user associated with the booking
    user = booking.employee

    # Get the booking user profile associated with the user
    booking_user_profile = BookingUserProfile.objects.get(pk=user.pk)

    # Get the lector associated with the booking
    lector = booking.lector

    # Get the training associated with the booking
    training = booking.booking_type

    html_message = render_to_string(
        'emails/email-update-booking-user.html',
        {
            'profile': booking_user_profile,
            'booking': booking,
            'lector': lector,
            'training': training,

        }
    )
    plain_message = strip_tags(html_message)
    send_mail(
        subject='CoachMe Successful booking update!',
        message=plain_message,
        html_message=html_message,
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=(
            user.email,
            'manukov.business@gmail.com',
        ),
    )


def send_email_to_lector_after_booking_update(booking):
    # Get the user associated with the booking
    user = booking.employee

    # Get the booking user profile associated with the user
    booking_user_profile = BookingUserProfile.objects.get(pk=user.pk)

    # Get the lector associated with the booking
    lector = booking.lector

    # Get the training associated with the booking
    training = booking.booking_type

    # Get the company associated with the employee
    company = Company.objects.filter(company_domain__iendswith=user.email.split('@')[1]).get()

    html_message = render_to_string(
        'emails/email-update-booking-lector.html',
        {
            'profile': booking_user_profile,
            'booking': booking,
            'lector': lector,
            'training': training,
            'company': company,
        }
    )
    plain_message = strip_tags(html_message)
    send_mail(
        subject='CoachMe A booking with you as a Lector was just updated!',
        message=plain_message,
        html_message=html_message,
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=(
            'manukov.business@gmail.com',
            lector.email,
        ),
    )


def send_email_to_user_after_booking_deletion(booking):
    # Get the user associated with the booking
    user = booking.employee

    # Get the booking user profile associated with the user
    booking_user_profile = BookingUserProfile.objects.get(pk=user.pk)

    # Get the lector associated with the booking
    lector = booking.lector

    # Get the training associated with the booking
    training = booking.booking_type

    html_message = render_to_string(
        'emails/email-delete-booking-user.html',
        {
            'profile': booking_user_profile,
            'booking': booking,
            'lector': lector,
            'training': training,

        }
    )
    plain_message = strip_tags(html_message)
    send_mail(
        subject='CoachMe Successful booking deletion!',
        message=plain_message,
        html_message=html_message,
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=(
            user.email,
            'manukov.business@gmail.com',
        ),
    )


def send_email_to_lector_after_booking_deletion(booking):
    # Get the user associated with the booking
    user = booking.employee

    # Get the booking user profile associated with the user
    booking_user_profile = BookingUserProfile.objects.get(pk=user.pk)

    # Get the lector associated with the booking
    lector = booking.lector

    # Get the training associated with the booking
    training = booking.booking_type

    # Get the company associated with the employee
    company = Company.objects.filter(company_domain__iendswith=user.email.split('@')[1]).get()

    html_message = render_to_string(
        'emails/email-delete-booking-lector.html',
        {
            'profile': booking_user_profile,
            'booking': booking,
            'lector': lector,
            'training': training,
            'company': company,
        }
    )
    plain_message = strip_tags(html_message)
    send_mail(
        subject='CoachMe A booking with you as a Lector was just deleted!',
        message=plain_message,
        html_message=html_message,
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=(
            'manukov.business@gmail.com',
            lector.email,
        ),
    )


# Signal for booking creation or update
@receiver(post_save, sender=Booking)
def booking_created(instance, created, **kwargs):
    if created:
        send_email_to_user_after_booking_creation(instance)
        send_email_to_lector_after_booking_creation(instance)
    elif not created:
        send_email_to_user_after_booking_update(instance)
        send_email_to_lector_after_booking_update(instance)


# Signal for booking deletion
@receiver(post_delete, sender=Booking)
def booking_deleted(instance, **kwargs):
    send_email_to_user_after_booking_deletion(instance)
    send_email_to_lector_after_booking_deletion(instance)


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


@receiver(post_save, sender=UserModel)
def user_created(instance, created, **kwargs):
    if created:
        send_email_after_successful_registration(instance)
