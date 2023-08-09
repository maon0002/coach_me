from django.core import validators
from django.db import models
from django.contrib.auth import get_user_model
from django.utils.timezone import now
from coach_me.accounts.models import BookingUser
from coach_me.bookings.validators import validate_phone_numbers_formatting, \
    validate_string_is_letters_and_hyphens_only, validate_string_is_letters_only
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
    PAID_MAX_LENGTH = 3
    PLATFORM_CHOICES = (
        ('Teams', 'Teams'),
        ('Zoom', 'Zoom'),
        ('Skype', 'Skype'),
        ('Google meetings', 'Google meetings'),
    )
    PLATFORM_CHOICES_MAX_LEN = max(len(choice[1]) for choice in PLATFORM_CHOICES)

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
    START_TIME_CHOICES_MAX_LEN = max(len(choice[1]) for choice in START_TIME_CHOICES)

    TRAINING_MODE_CHOICES = (
        ('Live', 'Live'),
        ('Online', 'Online'),
    )
    TRAINING_MODE_MAX_LEN = max(len(choice[1]) for choice in TRAINING_MODE_CHOICES)
    COMPANY_NAME_MAX_LEN = 75
    CERTIFICATE_CODE_MAX_LEN = 10
    LABEL_MAX_LEN = 30

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
        max_length=COMPANY_NAME_MAX_LEN,
        null=True,
        blank=True,
    )

    corporate_email = models.EmailField(
        null=True,
        blank=True,
        default=None,

    )

    employee = models.ForeignKey(
        BookingUser,
        on_delete=models.DO_NOTHING,
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
        max_length=TRAINING_MODE_MAX_LEN,
        default='Online',
        choices=TRAINING_MODE_CHOICES,
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
        max_length=CERTIFICATE_CODE_MAX_LEN,
        null=True,
        blank=True,
    )
    notes = models.TextField(
        null=True,
        blank=True,
    )
    date_scheduled = models.DateTimeField(
        auto_now_add=True,
    )
    label = models.CharField(
        max_length=LABEL_MAX_LEN,
        null=True,
        blank=True,
    )

    preferred_platforms = models.CharField(
        max_length=PLATFORM_CHOICES_MAX_LEN,
        null=True,
        blank=True,
        choices=(
            PLATFORM_CHOICES
        )
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

