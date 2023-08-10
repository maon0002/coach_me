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

    def __str__(self):
        return f'{self.email}'

    def __repr__(self):
        return f'{self.id}: {self.email}'
