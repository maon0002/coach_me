from django import forms
from django.contrib.auth import forms as auth_forms, get_user_model
from django.utils.translation import gettext_lazy as _
from coach_me.profiles.models import BookingUserProfile


UserModel = get_user_model()


class LoginUserForm(auth_forms.AuthenticationForm):

    username = forms.CharField(
        widget=forms.EmailInput(
            attrs={
                'style': 'border-color: blue;',
                'placeholder': 'Enter your email',
                # 'class': 'login-email',
                'class': 'form-control',
            }
        )
    )

    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                'style': 'border-color: blue;',
                'placeholder': 'Enter your password',
                'content': '*',
                # 'placeholder': '********',
                'autocomplete': 'off',
                # 'data-toggle': 'password',
                'render_value': True,
                'class': 'form-control',
            }
        )
    )

    class Meta(auth_forms.UserCreationForm.Meta):
        model = UserModel
        fields = '__all__'  # ('email', 'password')
        widgets = {
            'username': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'username pls',
                }),
            'password': forms.PasswordInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'pass pls',
                }),
        }


class RegisterUserForm(auth_forms.UserCreationForm):
    first_name = forms.CharField(
        label=_("First name"),
        widget=forms.TextInput(
            attrs={
                'style': 'border-color: blue;',
                'placeholder': 'First name',
                'title': 'First name',
                # 'label': 'First name',

            },
        )
    )

    last_name = forms.CharField(
        label=_("Last name"),
        widget=forms.TextInput(
            attrs={
                'style': 'border-color: blue;',
                'placeholder': 'Last name',
                # 'label': 'Last name',
            },
        )
    )

    email = forms.CharField(
        label=_("Corporate email"),
        widget=forms.EmailInput(
            attrs={
                'style': 'border-color: blue;',
                'placeholder': 'Enter your corporate email',
                # 'label': 'Corporate email',
            },
        )
    )

    password1 = forms.CharField(
        label=_("Password"),
        widget=forms.PasswordInput(
            attrs={
                'style': 'border-color: blue;',
                # 'placeholder': 'Password',
                # 'label': 'Password',
            },
        )
    )

    password2 = forms.CharField(
        label=_("Repeat Password"),
        widget=forms.PasswordInput(
            attrs={
                'style': 'border-color: blue;',
                'placeholder': 'Repeat password',
                "autocomplete": "new-password",
                # 'label': 'Repeat Password',
                # 'is_hidden': True,
                # "required": False,
            },
        )
    )

    consent_terms = forms.BooleanField(
        widget=forms.CheckboxInput,
        label=_("Agree to Terms and Conditions"),
    )
    newsletter_subscription = forms.BooleanField(
        widget=forms.CheckboxInput,
        label=_("Subscribe to our newsletter"),
        required=False,
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password1'].help_text = _('Please enter your password')
        self.fields['password2'].help_text = _('Please repeat your password')
        self.fields['email'].help_text = _('Use your company email address')

    def save(self, commit=True):
        user = super().save(commit)

        profile = BookingUserProfile(
            first_name=self.cleaned_data['first_name'],
            last_name=self.cleaned_data['last_name'],
            consent_terms=self.cleaned_data['consent_terms'],
            newsletter_subscription=self.cleaned_data['newsletter_subscription'],
            user=user,
        )
        if commit:
            profile.save()

        return user

    class Meta(auth_forms.UserCreationForm.Meta):
        model = UserModel
        fields = ['first_name', 'last_name', 'email', 'password1', 'password2']
        widgets = {
            'email': forms.TextInput(attrs={'class': 'form-control'}),
            'password': forms.PasswordInput(attrs={'class': 'form-control'}),
            'password1': forms.PasswordInput(attrs={'class': 'form-control'}),
            'password2': forms.PasswordInput(attrs={'class': 'form-control'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'consent_terms': forms.CheckboxInput(attrs={'class': 'form-check-input me-2'}),
            'newsletter_subscription': forms.CheckboxInput(attrs={'class': 'form-check-input me-2'}),
        }
