from django import forms
from django.contrib.auth import forms as auth_forms, get_user_model
from django.utils.translation import gettext_lazy as _
from coach_me.accounts.models import BookingUser
from coach_me.profiles.models import BookingUserProfile

UserModel = get_user_model()


class ProfileDashboardForm(forms.ModelForm):
    pass


class ProfileUpdateForm(forms.ModelForm):
    # date_of_birth = forms.DateField(
    #     widget=forms.DateInput(
    #         attrs={
    #             # 'class': 'form-control',
    #             'class': 'date-icon',
    #             'placeholder': 'YYYY-MM-DD',
    #         }
    #     ),
    #     label='Date of birth',
    #     required=False,  # Update this based on your requirements
    #     input_formats=['%Y-%m-%d'],  # Specify the date input format
    # )

    class Meta:
        model = BookingUserProfile
        # fields = '__all__'
        exclude = ['consent_terms', 'newsletter_subscription']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Hide the 'user' field
        self.fields['user'].widget = forms.HiddenInput()


class ProfileDeleteForm(forms.ModelForm):
    class Meta:
        model = BookingUserProfile
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Disable the 'user' field
        # self.fields['user'].disabled = True
        for field_name in self.fields:
            self.fields[field_name].widget.attrs['disabled'] = True


class ProfileDetailsForm(forms.ModelForm):
    class Meta:
        model = BookingUserProfile
        # fields = '__all__'
        exclude = ['user', 'consent_terms', 'newsletter_subscription']
