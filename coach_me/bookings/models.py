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


# TODO - move the profile models in the profile app
# class Company(models.Model):
#     MAX_COMPANY_SHORT_NAME = 20
#     MIN_COMPANY_SHORT_NAME = 2
#     MAX_COMPANY_LEGAL_NAME = 50
#     MIN_COMPANY_LEGAL_NAME = 3
#     MAX_CONTACT_PERSON_NAMES = 30
#     MAX_CONTACT_PERSON_ROLE_LEN = 15
#
#     short_company_name = models.CharField(
#         max_length=MAX_COMPANY_SHORT_NAME,
#         unique=True,
#         null=False,
#         blank=False,
#         validators=(
#             validators.MinLengthValidator(MIN_COMPANY_SHORT_NAME),
#             # validate_if_string_is_alphanumeric,
#         ),
#     )
#     legal_company_name = models.CharField(
#         max_length=MAX_COMPANY_SHORT_NAME,
#         unique=True,
#         null=False,
#         blank=False,
#         validators=(
#             validators.MinLengthValidator(MIN_COMPANY_LEGAL_NAME),
#         ),
#     )
#     company_register_number = models.PositiveBigIntegerField(
#         unique=True,
#
#     )
#     contact_person_names = models.CharField(
#         max_length=MAX_CONTACT_PERSON_NAMES
#     )
#     contact_person_role = models.CharField(
#         max_length=MAX_CONTACT_PERSON_ROLE_LEN
#     )
#     contact_person_email = models.EmailField()
#     contract_start_date = models.DateField()
#     contract_end_date = models.DateField()
#     company_domain = models.CharField(
#         max_length=30,
#         null=False,
#         blank=False,
#         default=None,
#     )
#
#     inserted_on = models.DateTimeField(auto_now_add=True)  # ,  auto_now=True for update
#     updated_on = models.DateTimeField(auto_now=True)  # ,  auto_now=True for update
#
#     def __str__(self):
#         return f'{self.id}: {self.short_company_name}'
#
#     class Meta:
#         verbose_name_plural = "Companies"


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

    # get_choices = MyModelMixin.get_distinct_choices('bookings.Booking', 'booking_type')[0]

    id = models.BigAutoField(primary_key=True)

    # employee = models.ForeignKey(
    #     UserModel,
    #     on_delete=models.DO_NOTHING)

    # user = models.ForeignKey(User, on_delete=models.RESTRICT, null=True, blank=True) # below
    # start_time = models.DateTimeField()  # datetime picker and check if it's free
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
    # company_name = models.ForeignKey(
    #     Company,
    #     on_delete=models.RESTRICT,
    #     default=None, )

    corporate_email = models.EmailField(
        null=True,
        blank=True,
        default=None,

    )
    # email = models.ForeignKey(
    #     UserModel,
    #     on_delete=models.DO_NOTHING)

    # email field as a ForeignKey to BookingUser model
    employee = models.ForeignKey(
        BookingUser,  # Use BookingUser model here
        on_delete=models.DO_NOTHING,
        # related_name='rel_bookings', #instead of employee_set
    )

    # pvt_email = models.CharField(max_length=50, null=False)
    private_email = models.EmailField(
        null=True,
        blank=True,
        verbose_name="Private email"
    )
    # pvt_email = models.ForeignKey(BookingUser, on_delete=models.RESTRICT)

    booking_type = models.ForeignKey(Training, on_delete=models.RESTRICT)

    # lector = models.CharField(
    #     max_length=200,
    #     null=False,
    #     blank=False,
    # )
    training_mode = models.CharField(
        max_length=10,
        default='Online',
        choices=(
            ('Live', 'Live'),
            ('Online', 'Online'),
        ),
    )
    lector = models.ForeignKey(Lector, on_delete=models.RESTRICT)

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

    inserted_on = models.DateTimeField(auto_now_add=True)  # ,  auto_now=True for update
    updated_on = models.DateTimeField(auto_now=True)  # ,  auto_now=True for update

    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)
        self.corporate_email = BookingUser.email
        self.first_name = Booking.first_name
        self.last_name = Booking.last_name

    # def clean(self):
    #     # Check if the booking being edited has changes in the employee or start time
    #     if self.pk is not None:
    #         original_booking = Booking.objects.get(pk=self.pk)
    #         if (
    #                 self.email == original_booking.email
    #                 and self.start_time == original_booking.start_time
    #         ):
    #             return  # Skip the validation if the employee and start time haven't changed
    #
    #     # Check if the start_time exists for the employee
    #     employee_availability_duplicate = Booking.objects.filter(
    #         email=self.id,
    #         start_date=self.start_date,
    #         start_time=self.start_time,
    #     ).exists()
    #
    #     # print(employee_availability_duplicate)
    #
    #     if employee_availability_duplicate:
    #         raise ValidationError("This start time is already booked for the employee.")
    #
    #     # Check if the start_time exists for the lector
    #     lector_availability_duplicate = Booking.objects.filter(
    #         lector=self.lector,
    #         start_date=self.start_date,
    #         start_time=self.start_time,
    #     ).exists()
    #
    #     if lector_availability_duplicate:
    #         raise ValidationError("This start time is already booked for this lector.")
    #
    #     # Check if the employee corporate email has the correct domain name suffix
    #     existing_domains = Company.objects.filter(
    #         company_domain__iendswith=str(self.email).split('@')[1]).exists()
    #     if not existing_domains:
    #         raise ValidationError(
    #             """
    #             We can't find your company domain in our database!
    #             Please contact our team for support or check if the corporate email address is correct!
    #             """
    #         )
    #
    #         # # Check if the start_time is greater then current datetime + 1 day  # TODO
    #         # lector_availability_duplicate = Booking.objects.filter(
    #         #     lector=self.lector,
    #         #     start_date=self.start_date,
    #         #     start_time=self.start_time,
    #         # ).exists()
    #         # if lector_availability_duplicate:
    #         #     raise ValidationError("This start time is already booked for this lector.")
    ###################MOVED TO THE BOOKING CREATION VIEW
    # def clean(self):
    #     # Check if the booking being edited has changes in the employee or start time
    #     if self.pk is not None:
    #         original_booking = Booking.objects.get(pk=self.pk)
    #         if (
    #                 self.employee == original_booking.employee
    #                 and self.start_time == original_booking.start_time
    #         ):
    #             return  # Skip the validation if the employee and start time haven't changed
    #
    #     # Check if the start_time exists for the employee
    #     # booking_user = self.request.user  # Access the BookingUser instance directly
    #
    #     # user = BookingUserProfile.objects.filter(pk=UserModel.pk).first()
    #
    #     employee_availability_duplicate = Booking.objects.filter(
    #         employee=self.employee,
    #         # employee=user,
    #         start_date=self.start_date,
    #         start_time=self.start_time,
    #     ).exists()
    #
    #     if employee_availability_duplicate:
    #         raise ValidationError("This start time is already booked for the employee.")
    #
    #     # Check if the start_time exists for the lector
    #     lector_availability_duplicate = Booking.objects.filter(
    #         lector=self.lector,
    #         start_date=self.start_date,
    #         start_time=self.start_time,
    #     ).exists()
    #
    #     if lector_availability_duplicate:
    #         raise ValidationError("This start time is already booked for this lector.")
    #
    #     # Check if the employee corporate email has the correct domain name suffix
    #     existing_domains = Company.objects.filter(
    #         company_domain__iendswith=str(self.employee.email).split('@')[1]
    #     ).exists()
    #     if not existing_domains:
    #         raise ValidationError(
    #             """
    #             We can't find your company domain in our database!
    #             Please contact our team for support or check if the corporate email address is correct!
    #             """
    #         )

    @property
    def user_full_name(self):
        return f"{self.first_name} {self.last_name}"

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)

    def __str__(self):
        # return f'{self.id}: {self.first_name} {self.last_name} --- {self.start_date} | {self.start_time}'
        return f'{self.employee}'
    #TODO apply later
    # class Meta:
    #     ordering = ('-start_date', '-start_time',)




###############MOVED
#
#
# class Training(models.Model):
#     MAX_SERVICE_NAME_LENGTH = 50
#     service_name = models.CharField(
#         max_length=MAX_SERVICE_NAME_LENGTH,
#         default=None,
#     )
#     service_description = models.TextField(default="Add training description")
#     service_image = models.URLField(default='https://freesvg.org/img/1380565395.png')
#
#     inserted_on = models.DateTimeField(auto_now_add=True)  # ,  auto_now=True for update
#     updated_on = models.DateTimeField(auto_now=True)  # ,  auto_now=True for update
#
#     def __str__(self):
#         return f'{self.service_name}'
#         # return f'{self.id}: {self.service_name}'
#
#
# class Lector(models.Model):
#     FIRST_NAME_MAX_LENGTH = 30
#     FIRST_NAME_MIN_LENGTH = 2
#     LAST_NAME_MAX_LENGTH = 30
#     LAST_NAME_MIN_LENGTH = 2
#     PHONE_MAX_LENGTH = 10
#
#     # #TODO to add constraint
#     # user = models.ForeignKey(
#     #     BookingUser,  # Use BookingUser model here
#     #     on_delete=models.DO_NOTHING,
#     #     # related_name='rel_bookings', #instead of employee_set
#     # )
#
#     first_name = models.CharField(
#         max_length=FIRST_NAME_MAX_LENGTH,
#         null=False,
#         blank=False,
#         default=None,
#         validators=(
#             validators.MinLengthValidator(FIRST_NAME_MIN_LENGTH),
#             validate_string_is_letters_only,
#         ),
#     )
#     last_name = models.CharField(
#         max_length=LAST_NAME_MAX_LENGTH,
#         null=False,
#         blank=False,
#         default=None,
#         validators=(
#             validators.MinLengthValidator(LAST_NAME_MIN_LENGTH),
#             validate_string_is_letters_and_hyphens_only,
#         ),
#     )
#     phone = models.CharField(
#         max_length=PHONE_MAX_LENGTH,
#         null=False,
#         blank=False,
#         default=None,
#         validators=(
#             validate_phone_numbers_formatting,
#         )
#     )
#
#     email = models.EmailField(
#         null=False,
#         blank=False,
#         default=None,
#     )
#     lector_image = models.URLField(default='https://img.freepik.com/free-icon/user_318-159711.jpg')
#     service_integrity = models.ManyToManyField(Training)
#
#     biography = models.TextField()
#
#     inserted_on = models.DateTimeField(auto_now_add=True)  # ,  auto_now=True for update
#     updated_on = models.DateTimeField(auto_now=True)  # ,  auto_now=True for update
#
#     @property
#     def full_name(self):
#         if self.first_name or self.last_name:
#             return f"{self.first_name} {self.last_name}"
#
#     def __str__(self):
#         # return f'{self.id}: {self.first_name} {self.last_name}'
#         return f'{self.first_name} {self.last_name}'
#
#     def __repr__(self):
#         return f'{self.id}: {self.first_name} {self.last_name}'
#
