from django.apps import apps
from django.contrib.auth.mixins import AccessMixin
from django.shortcuts import redirect
from django.shortcuts import get_object_or_404

from coach_me.accounts.models import BookingUser
from coach_me.profiles.models import BookingUserProfile


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


class DisabledFormFieldsMixin:
    disabled_fields = ()

    def get_form(self, *args, **kwargs):
        form = super().get_form(*args, **kwargs)

        # fields = self.disabled_fields \
        # if self.disabled_fields != '__all__' \
        # else

        for field in self.disabled_fields:
            form.fields[field].widget.attrs['disabled'] = 'disabled'
            form.fields[field].widget.attrs['readonly'] = 'readonly'

        return form


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
