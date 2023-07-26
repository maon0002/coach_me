from django.core import validators
from django.core.exceptions import ValidationError
from django.core.validators import MinLengthValidator
from django.db import models
from django.contrib.auth import models as auth_models, get_user_model
from coach_me.accounts.managers import BookingUserManager


# Create your models here.
class BookingUser(auth_models.AbstractBaseUser, auth_models.PermissionsMixin):
    email = models.EmailField(
        null=False,
        blank=False,
        unique=True,
        verbose_name="Corporate email",
    )

    date_joined = models.DateTimeField(
        auto_now_add=True,
    )

    is_staff = models.BooleanField(
        default=False,
    )

    USERNAME_FIELD = 'email'
    objects = BookingUserManager()

    # TODO move below to the view
    # def clean(self):
    #     # Check if the domain part from the corporate email matches the existed domains in Company
    #
    #     existing_domains = Company.objects.filter(
    #         company_domain__iendswith=self.email.split('@')[1]
    #     ).exists()
    #     if not existing_domains:
    #         raise ValidationError(
    #             """
    #             We can't find your company domain in our database!
    #             Please contact our team for support or check if the corporate email address is correct!
    #             """
    #         )

    def __str__(self):
        return f'{self.email}'
        # return f'{self.id}: {self.email}'

    def __repr__(self):
        return f'{self.id}: {self.email}'

# UserModel = get_user_model()

# TODO - move the profile models in the profile app
class Company(models.Model):
    MAX_COMPANY_SHORT_NAME = 20
    MIN_COMPANY_SHORT_NAME = 2
    MAX_COMPANY_LEGAL_NAME = 50
    MIN_COMPANY_LEGAL_NAME = 3
    MAX_CONTACT_PERSON_NAMES = 30
    MAX_CONTACT_PERSON_ROLE_LEN = 15

    short_company_name = models.CharField(
        max_length=MAX_COMPANY_SHORT_NAME,
        unique=True,
        null=False,
        blank=False,
        validators=(
            validators.MinLengthValidator(MIN_COMPANY_SHORT_NAME),
            # validate_if_string_is_alphanumeric,
        ),
        verbose_name="Short Company name",
    )
    legal_company_name = models.CharField(
        max_length=MAX_COMPANY_SHORT_NAME,
        unique=True,
        null=False,
        blank=False,
        validators=(
            validators.MinLengthValidator(MIN_COMPANY_LEGAL_NAME),
        ),
    )
    company_register_number = models.PositiveBigIntegerField(
        unique=True,

    )
    contact_person_names = models.CharField(
        max_length=MAX_CONTACT_PERSON_NAMES
    )
    contact_person_role = models.CharField(
        max_length=MAX_CONTACT_PERSON_ROLE_LEN
    )
    contact_person_email = models.EmailField()
    contract_start_date = models.DateField()
    contract_end_date = models.DateField()
    company_domain = models.CharField(
        max_length=30,
        null=False,
        blank=False,
        default=None,
    )

    inserted_on = models.DateTimeField(auto_now_add=True)  # ,  auto_now=True for update
    updated_on = models.DateTimeField(auto_now=True)  # ,  auto_now=True for update

    def __str__(self):
        return f'{self.id}: {self.short_company_name}'

    class Meta:
        verbose_name_plural = "Companies"
