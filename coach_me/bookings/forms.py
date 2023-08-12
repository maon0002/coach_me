from django import forms
from django.contrib.auth import get_user_model
from django.http import request
from django.shortcuts import get_object_or_404
from coach_me.bookings.form_mixins import FieldsWithFormControlClassMixin
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from coach_me.bookings.models import Booking
from django.forms import DateInput
from widget_tweaks.templatetags.widget_tweaks import render_field

UserModel = get_user_model()


class BookingForm(FieldsWithFormControlClassMixin, forms.ModelForm):
    form_control_fields = '__all__'

    class Meta:
        model = Booking
        exclude = ['email']


class BookingCreateForm(FieldsWithFormControlClassMixin, forms.ModelForm):
    form_control_fields = '__all__'

    class Meta:
        model = Booking
        fields = [
            'booking_type',
            'lector',
            'start_date',
            'start_time',
            'first_name',
            'last_name',
            'employee',
            'corporate_email',
            'phone',
            'training_mode',
            'lector',
            'price',
            'preferred_platforms',
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Hide the 'user' field
        self.fields['employee'].widget = forms.HiddenInput()
        # Set the attrs for date pickers
        self.fields['start_date'].widget = DateInput(
            attrs={'class': 'form-control', 'id': 'datepicker'}
        )

        self.fields['start_date'].help_text = _('*the format is : "YYYY-MM-DD"')
        self.fields['lector'].help_text = _('Please check if the selected lector is available for the training')
        self.fields['preferred_platforms'].help_text = _('Please add one or more platforms')

    def clean_start_date(self):
        start_date = self.cleaned_data.get('start_date')

        # Get the current date
        today = timezone.now().date()

        # Check if the start_date is at least one day later than the current date
        if start_date <= today:
            raise forms.ValidationError("Start date should be at least one day later than the current date.")

        return start_date

    def render_field(self, field, **kwargs):
        return render_field(field, **kwargs)


class BookingDeleteForm(forms.ModelForm):
    class Meta:
        model = Booking
        exclude = ['employee']


class BookingDetailsForm(FieldsWithFormControlClassMixin, forms.ModelForm):
    form_control_fields = '__all__'

    class Meta:
        model = Booking
        fields = '__all__'


class BookingUpdateForm(FieldsWithFormControlClassMixin, forms.ModelForm):
    form_control_fields = '__all__'

    class Meta:
        model = Booking
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Hide the 'user' field
        self.fields['employee'].widget = forms.HiddenInput()
        # Set the attrs for date pickers
        self.fields['start_date'].widget = DateInput(
            attrs={'class': 'form-control', 'id': 'datepicker'}
        )

    def clean_start_date(self):
        start_date = self.cleaned_data.get('start_date')

        # Get the current date
        today = timezone.now().date()

        # Check if the start_date is at least one day later than the current date
        if start_date <= today:
            raise forms.ValidationError("Start date should be at least one day later than the current date.")

        return start_date

    def render_field(self, field, **kwargs):
        return render_field(field, **kwargs)
