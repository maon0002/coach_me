from django.core.exceptions import ValidationError
from django.core import validators
from django.db import models
# Create your models here.
from django.contrib.auth import get_user_model
from django.utils.timezone import now
from django.core.mail import send_mail
from coach_me.accounts.models import BookingUser
from coach_me.bookings.validators import validate_if_string_is_alphanumeric, validate_phone_numbers_formatting, \
    validate_string_is_letters_and_hyphens_only, validate_string_is_letters_only
from coach_me.bookings.mixins import MyModelMixin
from coach_me.lectors.models import Lector
from coach_me.profiles.models import BookingUserProfile, Company
from coach_me.trainings.models import Training

UserModel = get_user_model()

class Booking(models.Model):
    FIRST_NAME_MAX_LENGTH = 30
    FIRST_NAME_MIN_LENGTH = 2
    LAST_NAME_MAX_LENGTH = 30
    LAST_NAME_MIN_LENGTH = 2
    PHONE_MAX_LENGTH = 10
    PAID_CHOICES = (
        ('Yes', 'Yes'),
        ('No', 'No'),
    )
    PAID_MAX_LENGTH = max([len(list(choice[1])) for choice in PAID_CHOICES])
    START_TIME_CHOICES = (
        ('09:00:00', '09:00:00'),
        ('10:00:00', '10:00:00'),
        ('11:00:00', '11:00:00'),
        ('12:00:00', '12:00:00'),
        ('13:00:00', '13:00:00'),
        ('14:00:00', '14:00:00'),
        ('15:00:00', '15:00:00'),
        ('16:00:00', '16:00:00'),
        ('17:00:00', '17:00:00'),
        ('18:00:00', '18:00:00'),
    )

    id = models.BigAutoField(primary_key=True)

    start_date = models.DateField(default=now, )  # datetime picker and check if it's free
    start_time = models.CharField(
        null=False,
        blank=False,
        choices=START_TIME_CHOICES,
        max_length=8,

    )  # datetime picker and check if it's free
    first_name = models.CharField(
        max_length=FIRST_NAME_MAX_LENGTH,
        null=False,
        blank=False,
        validators=(
            validators.MinLengthValidator(FIRST_NAME_MIN_LENGTH),
            validate_string_is_letters_only,
        ),

    )
    last_name = models.CharField(
        max_length=LAST_NAME_MAX_LENGTH,
        null=False,
        blank=False,
        validators=(
            validators.MinLengthValidator(LAST_NAME_MIN_LENGTH),
            validate_string_is_letters_and_hyphens_only,

        ),
    )
    phone = models.CharField(
        max_length=PHONE_MAX_LENGTH,
        null=False,
        blank=False,
        validators=(
            validate_phone_numbers_formatting,
        )
    )
    company_name = models.CharField(
        max_length=200,
        # null=True
    )

    corporate_email = models.EmailField(
        null=True,
        blank=True,
        default=None,

    )

    # email field as a ForeignKey to BookingUser model
    employee = models.ForeignKey(
        BookingUser,  # Use BookingUser model here
        on_delete=models.DO_NOTHING,
        # related_name='rel_bookings', #instead of employee_set
    )

    private_email = models.EmailField(
        null=True,
        blank=True,
        verbose_name="Private email"
    )

    booking_type = models.ForeignKey(
        Training,
        on_delete=models.DO_NOTHING
    )

    training_mode = models.CharField(
        max_length=10,
        default='Online',
        choices=(
            ('Live', 'Live'),
            ('Online', 'Online'),
        ),
    )
    lector = models.ForeignKey(
        Lector,
        on_delete=models.DO_NOTHING
    )

    price = models.DecimalField(
        default=0,
        decimal_places=2,
        max_digits=10,
    )
    paid = models.CharField(
        max_length=PAID_MAX_LENGTH,
        null=True,
        blank=True,
        default='No',
        choices=(
            PAID_CHOICES
        ),
    )
    amount_paid_online = models.DecimalField(
        default=0,
        decimal_places=2,
        max_digits=10,
    )
    certificate_code = models.CharField(
        max_length=50,
        null=True,
        blank=True,
    )
    notes = models.TextField(
        null=True,
        blank=True,
    )
    date_scheduled = models.DateTimeField(
        auto_now_add=True,
    )  # ,  auto_now=True for update
    label = models.CharField(
        max_length=50,
        null=True,
        blank=True,
    )

    preferred_platforms = models.CharField(
        max_length=30,
        null=True,
        blank=True,
    )

    inserted_on = models.DateTimeField(
        auto_now_add=True
    )  # ,  auto_now=True for update
    updated_on = models.DateTimeField(
        auto_now=True
    )  # ,  auto_now=True for update

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.corporate_email = BookingUser.email
        self.first_name = Booking.first_name
        self.last_name = Booking.last_name
        self.full_name = f"{self.first_name} {self.last_name}"

    @property
    def user_full_name(self):
        return f"{str(self.first_name)} {str(self.last_name)}"

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.employee}'
    # TODO apply later
    # class Meta:
    #     ordering = ('-start_date', '-start_time',)
