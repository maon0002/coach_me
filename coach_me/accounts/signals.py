from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.template.loader import render_to_string
from django.utils.html import strip_tags

UserModel = get_user_model()


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


# @receiver(post_save, **kwargs)
@receiver(post_save, sender=UserModel)
# def user_created(instance, created):
def user_created(instance, created, **kwargs):
    # print("INSTANCE>>>>>>>", instance)
    # print("Created>>>>>>>", created)

    if created:
        send_email_after_successful_registration(instance)


# args
# ()
# kwargs
# {'created': True,
#  'instance': 17: manukov.business@gmail.com,
#  'raw': False,
#  'sender': <class 'coach_me.accounts.models.BookingUser'>,
#  'signal': <django.db.models.signals.ModelSignal object at 0x0396F448>,
#  'update_fields': None,
#  'using': 'default'}