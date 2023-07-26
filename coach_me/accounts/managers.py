from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.hashers import make_password

#
# class BookingUserManager(BaseUserManager):
#     use_in_migrations = True
#
#     def create_user(self, email, password=None, **extra_fields):
#         if not email:
#             raise ValueError("The Email field must be set")
#         email = self.normalize_email(email)
#         user = self.model(email=email, **extra_fields)
#         user.set_password(password)
#         user.save()
#         return user
#
#     def create_superuser(self, email, password=None, **extra_fields):
#         extra_fields.setdefault('is_staff', True)
#         extra_fields.setdefault('is_superuser', True)
#         return self.create_user(email, password, **extra_fields)


class BookingUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(email, password, **extra_fields)

#
# class BookingUser(AbstractBaseUser, PermissionsMixin):
#     employee = models.CharField(max_length=100)  # Add the 'employee' field here
#     email = models.EmailField(
#         null=False,
#         blank=False,
#         unique=True,
#         verbose_name="Corporate email",
#     )
#
#     date_joined = models.DateTimeField(
#         auto_now_add=True,
#     )
#
#     is_staff = models.BooleanField(
#         default=False,
#     )
#
#     USERNAME_FIELD = 'email'
#     objects = BookingUserManager()
#
#     def clean(self):
#         # Check if the domain part from the corporate email matches the existed domains in Company
#         existing_domains = Company.objects.filter(
#             company_domain__iendswith=self.email.split('@')[1]
#         ).exists()
#         if not existing_domains:
#             raise ValidationError(
#                 """
#                 We can't find your company domain in our database!
#                 Please contact our team for support or check if the corporate email address is correct!
#                 """
#             )
#
#     def __str__(self):
#         return f'{self.id}: {self.email}'
