from django import forms
from django.contrib.auth import get_user_model
from django.http import request
from django.shortcuts import get_object_or_404
from django.utils import timezone

from coach_me.bookings.models import Booking
from coach_me.profiles.models import BookingUserProfile

UserModel = get_user_model()


class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        # fields = ['date', 'start_time', 'end_time']
        exclude = ['email']


# class BookingCreateForm(forms.ModelForm):
#     # first_name = forms.CharField(
#     #     max_length=30,
#     #     widget=forms.TextInput(attrs={'placeholder': 'First name'}),
#     # )
#     class Meta:
#         model = Booking
#         # exclude = ['employee']
#         # fields = ['start_date', 'employee', 'other_fields']
#         fields = '__all__'
#
#     # class Meta:
#     #     model = Booking
#     #     # fields = ['date', 'start_time', 'end_time']
#     #     exclude = ['employee']
#     #     # fields = '__all__'


# class BookingCreateForm(forms.ModelForm):
#     class Meta:
#         model = Booking
#         fields = '__all__'
#         # exclude = ['employee']
#
#     def __init__(self, *args, **kwargs):
#         # Get the logged-in user and pass it as a keyword argument to the form
#         self.employee = kwargs.pop('employee', None)
#         super().__init__(*args, **kwargs)
#
#     def save(self, commit=True):
#         # Set the employee field to the logged-in user before saving
#         instance = super().save(commit=False)
#         instance.employee = self.employee
#         if commit:
#             instance.save()
#         return instance


# from django import forms
# from .models import Booking

# class BookingCreateForm(forms.ModelForm):
#     # Other form fields and configurations here...
#
#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         # Hide the 'user' field
#         self.fields['employee'].widget = forms.HiddenInput()
#
#     #
#     def save(self, commit=True):
#         # Set the employee field to the user before saving
#
#         instance = super().save(commit=False)
#         # instance.corporate_email = self.initial['']
#         instance.corporate_email = self.initial['email']
#         # print(self.initial['email'])
#         if commit:
#             instance.save()
#         return instance
#
#     class Meta:
#         model = Booking
#         fields = '__all__'
#
#     # def __init__(self, *args, **kwargs):
#     #     user_email = kwargs.pop('', None)
#     #     super().__init__(*args, **kwargs)
#     #
#     #     # Hide the 'email' field
#     #     # self.fields['email'].widget = forms.HiddenInput()
#     #
#     #     # Set the initial value for the 'email' field as the user's email
#     #     if user_email:
#     #         self.initial['email'] = user_email
#     #
#     # def save(self, commit=True):
#     #     # Set the employee field to the user before saving
#     #     instance = super().save(commit=False)
#     #     # instance.email_id = self.initial['email']
#     #     if commit:
#     #         instance.save()
#     #     return instance
#
# from django import forms
# from .models import Booking


class BookingCreateForm(forms.ModelForm):
    class Meta:
        model = Booking
        # fields = '__all__'
        fields = [
            'start_date',
            'start_time',
            'first_name',
            'last_name',
            'employee',
            'corporate_email',
            'phone',
            'booking_type',
            'training_mode',
            'lector',
            'price',
            'preferred_platforms',
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Hide the 'user' field
        self.fields['employee'].widget = forms.HiddenInput()

    def clean_start_date(self):
        start_date = self.cleaned_data.get('start_date')

        # Get the current date
        today = timezone.now().date()

        # Check if the start_date is at least one day later than the current date
        if start_date <= today:
            raise forms.ValidationError("Start date should be at least one day later than the current date.")

        return start_date


class BookingDeleteForm(forms.ModelForm):
    class Meta:
        model = Booking
        # fields = ['date', 'start_time', 'end_time']
        exclude = ['employee']
        # fields = '__all__'


class BookingDetailsForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = '__all__'


class BookingUpdateForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = '__all__'
        # exclude = ['consent_terms', 'newsletter_subscription']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Hide the 'user' field
        self.fields['employee'].widget = forms.HiddenInput()

    def clean_start_date(self):
        start_date = self.cleaned_data.get('start_date')

        # Get the current date
        today = timezone.now().date()

        # Check if the start_date is at least one day later than the current date
        if start_date <= today:
            raise forms.ValidationError("Start date should be at least one day later than the current date.")

        return start_date
