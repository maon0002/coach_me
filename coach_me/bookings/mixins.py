from django.apps import apps
from django.contrib.auth.mixins import AccessMixin
from django.shortcuts import redirect
from django.shortcuts import get_object_or_404

from coach_me.accounts.models import BookingUser
from coach_me.lectors.models import Lector
from coach_me.profiles.models import BookingUserProfile
from coach_me.trainings.models import Training


class DefineModelsMixin:


    def get_booking_user_profile(self, *args, **kwargs):
        # Get the primary key (pk) of the logged-in user
        user_pk = self.request.user.pk

        # Retrieve the BookingUserProfile using the pk
        # booking_user_profile = get_object_or_404(BookingUserProfile, user_id=user_pk)
        booking_user_profile = BookingUserProfile.objects.filter(pk=user_pk)
        if booking_user_profile:
            return booking_user_profile
        else:
            return None

    def get_booking_user(self, *args, **kwargs):
        # Get the primary key (pk) of the logged-in user
        user_pk = self.request.user.pk

        # Retrieve the BookingUser using the pk
        # booking_user_profile = get_object_or_404(BookingUserProfile, user_id=user_pk)
        booking_user = BookingUser.objects.filter(pk=user_pk)

        if booking_user:
            return booking_user
        else:
            return None

    @staticmethod
    def get_lectors_by_training(training, list_csv):

        if Lector.objects.filter(service_integrity=training).all():
            available_lectors = Lector.objects.filter(service_integrity=training).all()
        else:
            return None

        if list_csv:
            available_lectors_lst = [x.full_name for x in available_lectors]
            return ", ".join(available_lectors_lst)

        return available_lectors

    @staticmethod
    def get_trainings_by_lector(lector, list_csv):
        if lector.service_integrity.exists():
            available_trainings = lector.service_integrity.all()
        else:
            return None

        if list_csv:
            available_trainings_lst = [x.service_name for x in available_trainings]
            return ", ".join(available_trainings_lst)

        return available_trainings


class MyModelMixin:
    @staticmethod
    def get_distinct_choices(model_name, field_name):
        model_class = apps.get_model(model_name)
        choices = tuple(model_class.objects.values_list(field_name, field_name).distinct())
        choices_list = list(model_class.objects.values_list(field_name).distinct())
        max_len = max(len(str(value)) for value in choices_list)
        return max_len, choices


class AnonymousRequiredMixin(AccessMixin):
    """
    Mixin to restrict access to views only for anonymous users (unauthenticated users).
    """

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect(
                'index')
        return super().dispatch(request, *args, **kwargs)


