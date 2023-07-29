from django.db import models
from django.contrib.auth import models as auth_models
from coach_me.accounts.managers import BookingUserManager


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

    def __repr__(self):
        return f'{self.id}: {self.email}'
