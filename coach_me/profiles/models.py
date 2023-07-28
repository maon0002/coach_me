from django.core import validators
from django.core.validators import MinLengthValidator
from django.db import models
from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from coach_me.accounts.models import BookingUser
# from coach_me.profiles.models import Company

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
