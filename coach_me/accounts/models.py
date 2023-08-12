from django.db import models
from django.contrib.auth import models as auth_models
from coach_me.accounts.managers import BookingUserManager
from django.contrib.auth.models import AbstractUser, Group


class BookingUser(auth_models.AbstractBaseUser, auth_models.PermissionsMixin):
    GROUP_CHOICES = (
        ('COACHME_STAFF', 'COACHME_STAFF'),
        ('COACHME_LECTOR', 'COACHME_LECTOR'),
        ('COACHME_USER', 'COACHME_USER'),
    )
    GROUPS_CHOICES_MAX_LEN = max(len(choice[1]) for choice in GROUP_CHOICES)
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
    #
    # groups = models.ManyToManyField(
    #     Group,
    #     blank=True,
    #     related_name='users',
    # )
    #
    c_labels = models.CharField(
        max_length=GROUPS_CHOICES_MAX_LEN,
        null=True,
        blank=True,
        default='COACHME_USER',
        choices=(
            GROUP_CHOICES
        ),
        verbose_name="COACHME Groups",
    )

    USERNAME_FIELD = 'email'
    objects = BookingUserManager()

    def __str__(self):
        return f'{self.email}'

    def __repr__(self):
        return f'ID {self.id}: {self.email}'
