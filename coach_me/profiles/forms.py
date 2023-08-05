from django import forms
from django.contrib.auth import forms as auth_forms, get_user_model
from django.utils.translation import gettext_lazy as _
from coach_me.accounts.models import BookingUser
from coach_me.profiles.models import BookingUserProfile, Company

UserModel = get_user_model()


class ProfileDashboardForm(forms.ModelForm):
    pass


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = BookingUserProfile
        exclude = ['consent_terms', 'newsletter_subscription', 'is_lector']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Hide the 'user' field
        self.fields['user'].widget = forms.HiddenInput()
        self.fields['date_of_birth'].help_text = _('in "YYYY-MM-DD" format')
        self.fields['phone'].help_text = _('starting with +359  (e.g "+35912345678")')


class ProfileDeleteForm(forms.ModelForm):
    class Meta:
        model = BookingUserProfile
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name in self.fields:
            self.fields[field_name].widget.attrs['disabled'] = True


class ProfileDetailsForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Hide the 'user' field
        self.fields['is_lector'].widget = forms.HiddenInput()

    class Meta:
        model = BookingUserProfile
        exclude = [
            # 'user',
            'consent_terms',
            'newsletter_subscription',
            'is_lector',
        ]


class CompanyListForm(forms.ModelForm):
    class Meta:
        model = Company
        # exclude = ['consent_terms', 'newsletter_subscription', 'is_lector']
        fields = '__all__'


class CompanyUpdateForm(forms.ModelForm):
    class Meta:
        model = Company
        fields = '__all__'
        # exclude = ['consent_terms', 'newsletter_subscription', 'is_lector']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # # Hide the 'user' field
        # self.fields['user'].widget = forms.HiddenInput()
        # self.fields['date_of_birth'].help_text = _('in "YYYY-MM-DD" format')
        # self.fields['phone'].help_text = _('starting with +359  (e.g "+35912345678")')


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
        # Hide the 'user' field
        # self.fields['is_lector'].widget = forms.HiddenInput()

    class Meta:
        model = Company
        # exclude = [
        #     # 'user',
        #     'consent_terms',
        #     'newsletter_subscription',
        #     'is_lector',
        # ]
        fields = '__all__'
