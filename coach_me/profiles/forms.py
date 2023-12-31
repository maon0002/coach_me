from django import forms
from django.contrib.auth import get_user_model
from django.forms import DateInput
from django.utils.translation import gettext_lazy as _
from widget_tweaks.templatetags.widget_tweaks import render_field
from coach_me.profiles.models import BookingUserProfile, Company

UserModel = get_user_model()


class ProfileUpdateForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Set the attrs for date pickers
        self.fields['date_of_birth'].widget = DateInput(
            attrs={'class': 'form-control', 'id': 'datepickerPast'}
        )

        # Hide the 'user' field
        self.fields['user'].widget = forms.HiddenInput()
        self.fields['date_of_birth'].help_text = _('in "YYYY-MM-DD" format')
        self.fields['phone'].help_text = _('starting with +359  (e.g "+35912345678")')

    def render_field(self, field, **kwargs):
        return render_field(field, **kwargs)

    class Meta:
        model = BookingUserProfile
        exclude = [
            'company',
            'consent_terms',
            'newsletter_subscription',
            'is_lector',
        ]


class ProfileDeleteForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name in self.fields:
            self.fields[field_name].widget.attrs['disabled'] = True

    class Meta:
        model = BookingUserProfile
        fields = '__all__'


class ProfileDetailsForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Hide the 'user' field
        self.fields['is_lector'].widget = forms.HiddenInput()
        self.fields['company'].widget = forms.HiddenInput()

    class Meta:
        model = BookingUserProfile
        exclude = [
            'company',
            'consent_terms',
            'newsletter_subscription',
            'is_lector',
        ]


class CompanyListForm(forms.ModelForm):
    class Meta:
        model = Company
        fields = '__all__'


class CompanyUpdateForm(forms.ModelForm):
    class Meta:
        model = Company
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class CompanyDeleteForm(forms.ModelForm):
    class Meta:
        model = Company
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name in self.fields:
            self.fields[field_name].widget.attrs['disabled'] = True


class CompanyDetailsForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    class Meta:
        model = Company
        fields = '__all__'
