from django import forms
from django.contrib.auth import forms as auth_forms, get_user_model
from django.utils.translation import gettext_lazy as _
from coach_me.accounts.models import BookingUser
from coach_me.lectors.models import Lector
from coach_me.profiles.models import BookingUserProfile

UserModel = get_user_model()


class LectorDashboardForm(forms.ModelForm):
    pass


class LectorList(forms.ModelForm):
    class Meta:
        model = Lector
        fields = '__all__'


class LectorUpdateForm(forms.ModelForm):
    class Meta:
        model = BookingUserProfile
        # fields = '__all__'
        exclude = ['consent_terms', 'newsletter_subscription', 'is_lector']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Hide the 'user' field
        self.fields['user'].widget = forms.HiddenInput()
        self.fields['date_of_birth'].help_text = _('in "YYYY-MM-DD" format')
        self.fields['phone'].help_text = _('starting with +359  (e.g "+35912345678")')
        # self.fields['email'].help_text = _('Use your company email address')


class LectorDeleteForm(forms.ModelForm):
    class Meta:
        model = Lector
        fields = '__all__'


class LectorDetailsForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Hide the 'user' field
        self.fields['is_lector'].widget = forms.HiddenInput()

    class Meta:
        model = Lector
        # fields = '__all__'
        exclude = ['user', 'consent_terms', 'newsletter_subscription', 'is_lector', ]
