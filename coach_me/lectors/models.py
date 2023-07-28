from django.core import validators
from django.db import models

from coach_me.accounts.models import BookingUser
from coach_me.trainings.models import Training
from coach_me.bookings.validators import validate_string_is_letters_only, \
    validate_string_is_letters_and_hyphens_only, \
    validate_phone_numbers_formatting


class Lector(models.Model):
    FIRST_NAME_MAX_LENGTH = 30
    FIRST_NAME_MIN_LENGTH = 2
    LAST_NAME_MAX_LENGTH = 30
    LAST_NAME_MIN_LENGTH = 2
    PHONE_MAX_LENGTH = 10

    # #TODO to add constraint
    user = models.ForeignKey(
        BookingUser,  # Use BookingUser model here
        on_delete=models.DO_NOTHING,
        # related_name='rel_bookings', #instead of employee_set
    )

    first_name = models.CharField(
        max_length=FIRST_NAME_MAX_LENGTH,
        null=False,
        blank=False,
        default=None,
        validators=(
            validators.MinLengthValidator(FIRST_NAME_MIN_LENGTH),
            validate_string_is_letters_only,
        ),
    )
    last_name = models.CharField(
        max_length=LAST_NAME_MAX_LENGTH,
        null=False,
        blank=False,
        default=None,
        validators=(
            validators.MinLengthValidator(LAST_NAME_MIN_LENGTH),
            validate_string_is_letters_and_hyphens_only,
        ),
    )
    phone = models.CharField(
        max_length=PHONE_MAX_LENGTH,
        null=False,
        blank=False,
        default=None,
        validators=(
            validate_phone_numbers_formatting,
        )
    )

    email = models.EmailField(
        null=False,
        blank=False,
        default=None,
    )
    lector_image = models.URLField(default='https://img.freepik.com/free-icon/user_318-159711.jpg')
    service_integrity = models.ManyToManyField(Training)

    biography = models.TextField()

    inserted_on = models.DateTimeField(auto_now_add=True)  # ,  auto_now=True for update
    updated_on = models.DateTimeField(auto_now=True)  # ,  auto_now=True for update

    @property
    def full_name(self):
        if self.first_name or self.last_name:
            return f"{self.first_name} {self.last_name}"

    def __str__(self):
        # return f'{self.id}: {self.first_name} {self.last_name}'
        return f'{self.first_name} {self.last_name}'

    def __repr__(self):
        return f'{self.id}: {self.first_name} {self.last_name}'
