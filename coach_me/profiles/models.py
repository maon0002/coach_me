from django.core.validators import MinLengthValidator
from django.db import models
from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from coach_me.accounts.models import BookingUser, Company

UserModel = get_user_model()


class BookingUserProfile(models.Model):
    MALE = 'Male'
    FEMALE = 'Female'
    DO_NOT_SHOW = 'Do not show'

    GENDERS = [(x, x) for x in (MALE, FEMALE, DO_NOT_SHOW)]

    user = models.OneToOneField(
        # BookingUser,
        UserModel,
        on_delete=models.CASCADE,
        primary_key=True,
    )

    first_name = models.CharField(
        max_length=30,
        validators=(
            MinLengthValidator(2),
        ),
        verbose_name='First Name',
    )

    last_name = models.CharField(
        max_length=30,
        validators=(
            MinLengthValidator(2),
        ),
        verbose_name='Last Name',
    )

    picture = models.URLField(
        default='https://img.freepik.com/premium-vector/colored-silhouette-man-s-head-isolated-white-background_764382-618.jpg',
        # default='/static/images/missing-person.jpg',
        null=True,
        blank=True,
    )

    date_of_birth = models.DateField(
        null=True,
        blank=True,
        default='1999-12-31'  # now() #django.utils.timezone.now
    )

    private_email = models.EmailField(  # TODO fix the below code and add validator
        null=True,
        blank=True,
        default=None,
    )

    phone = models.CharField(  # TODO fix the below code
        default='+359',
        max_length=10,
        # validators=(
        #     MinLengthValidator(10),
        # )
    )
    company = models.CharField(
        default=None,
        null=True,
        blank=True,
        max_length=30,
    )
    # company = models.ForeignKey(
    #     Company,
    #     on_delete=models.RESTRICT,
    #     default=None, )
    # company_id = models.ForeignKey(Company, on_delete=models.SET_NULL, null=True)
    # company = models.ForeignKey(
    #     Company,
    #     on_delete=models.RESTRICT,
    #     default=None,
    # )
    gender = models.CharField(
        max_length=max(len(x) for x, _ in GENDERS),
        choices=GENDERS,
        null=True,
        blank=True,
        default=DO_NOT_SHOW,
    )

    consent_terms = models.BooleanField(
        default=False,
    )
    newsletter_subscription = models.BooleanField(
        default=False,
        null=True,
        blank=True,
    )

    @property
    def full_name(self):
        if self.first_name or self.last_name:
            return f"{self.first_name} {self.last_name}"
        else:
            return None

    def __str__(self):
        return f'{self.first_name} {self.last_name}'
