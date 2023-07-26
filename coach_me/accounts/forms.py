from django import forms
from django.contrib.auth import forms as auth_forms, get_user_model
from django.utils.translation import gettext_lazy as _
from coach_me.accounts.models import BookingUser
from coach_me.profiles.models import BookingUserProfile

UserModel = get_user_model()


class LoginUserForm(auth_forms.AuthenticationForm):
    # # pass
    # email = forms.CharField(
    #     widget=forms.TextInput(
    #         attrs={
    #             'class': 'login-email'
    #         })
    # )

    username = forms.CharField(
        widget=forms.EmailInput(
            attrs={
                'style': 'border-color: blue;',
                'placeholder': 'Enter your email',
            })
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
            })
    )

    # pass

    #
    # password = forms.CharField(
    #     label=_("Repeat Password"),
    #     widget=forms.PasswordInput(attrs={"autocomplete": "new-password"}),
    #     strip=False,
    #     help_text=_("Repeat password, please"),
    # )

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
    # class Meta(auth_forms.AuthenticationForm.Meta):


# class RegisterUserForm(auth_forms.UserCreationForm):
#     class Meta:
#         model = UserModel
#         fields = ('username', 'email', 'password1', 'password')
#         # widgets = {
#         #     'username': forms.TextInput(attrs={
#         #         'class': 'ala-bala'
#         #     })
#         # }
#
#
# class RegisterUserForm(auth_forms.UserCreationForm):
#     first_name = forms.CharField(
#         max_length=30,
#         required=True
#     )
#
#     last_name = forms.CharField(
#         max_length=30,
#         required=True
#     )
#
#     password2 = forms.CharField(
#         label=_("Repeat Password"),
#         widget=forms.PasswordInput(
#             attrs={
#                 "autocomplete": "new-password",
#             }),
#         strip=False,
#         help_text=_("Repeat password, please"),
#     )
#
#     consent_terms = forms.BooleanField()
#     newsletter_subscription = forms.BooleanField()
#
#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         self.fields['password1'].help_text = _('It works')
#
#     def save(self, commit=True):
#         user = super().save(commit)
#
#         profile = BookingUser(
#             first_name=self.cleaned_data['first_name'],
#             last_name=self.cleaned_data['last_name'],
#             consent_terms=self.cleaned_data['consent_terms'],
#             newsletter_subscription=self.cleaned_data['newsletter_subscription'],
#
#             user=user,
#         )
#         if commit:
#             profile.save()
#
#         return user
#
#     class Meta(auth_forms.UserCreationForm.Meta):
#         model = UserModel
#         fields = ('email', 'password')
#         widgets = {
#             'email': forms.TextInput(attrs={'class': 'form-control'}),
#             'password': forms.PasswordInput(attrs={'class': 'form-control'}),
#             'first_name': forms.TextInput(attrs={'class': 'form-control'}),
#             'last_name': forms.TextInput(attrs={'class': 'form-control'}),
#             # 'password': forms.PasswordInput(attrs={'class': 'form-control'}),
#             # 'password': forms.PasswordInput(attrs={'class': 'form-control'}),
#         }

# Original which works
# class RegisterUserForm(auth_forms.UserCreationForm):
#     first_name = forms.CharField(
#         max_length=30,
#         required=True
#     )
#     last_name = forms.CharField(
#         max_length=30,
#         required=True
#     )
#
#     password2 = forms.CharField(
#         label=_("Repeat Password"),
#         widget=forms.PasswordInput(attrs={"autocomplete": "new-password"}),
#         strip=False,
#         help_text=_("Repeat password, please"),
#     )
#
#     consent_terms = forms.BooleanField()
#     newsletter_subscription = forms.BooleanField()
#
#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         self.fields['password1'].help_text = _('It works')
#
#     def save(self, commit=True):
#         user = super().save(commit)
#
#         profile = BookingUserProfile(
#             first_name=self.cleaned_data['first_name'],
#             last_name=self.cleaned_data['last_name'],
#             consent_terms=self.cleaned_data['consent_terms'],
#             newsletter_subscription=self.cleaned_data['newsletter_subscription'],
#             user=user,
#         )
#         if commit:
#             profile.save()
#
#         return user
#
#     class Meta(auth_forms.UserCreationForm.Meta):
#         model = UserModel
#         fields = ('email',)
#         widgets = {
#             'email': forms.TextInput(attrs={'class': 'form-control'}),
#             'password': forms.PasswordInput(attrs={'class': 'form-control'}),
#             'first_name': forms.TextInput(attrs={'class': 'form-control'}),
#             'last_name': forms.TextInput(attrs={'class': 'form-control'}),
#             # 'consent_terms': forms.BooleanField(attrs={'class': 'form-control'}),
#             # 'newsletter_subscription': forms.BooleanField(attrs={'class': 'form-control'}),
#         }


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

    # _password2 = forms.CharField(
    #     label=_("Repeat Password"),
    #     widget=forms.PasswordInput(attrs={"autocomplete": "new-password"}),
    #     strip=False,
    #     # help_text=_("Repeat password, please"),
    # )

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
        # self.fields['email'].help_text = _('Use your company email address')
        # self.fields['email'].help_text = _('Use your company email address')
        # self.fields['password2'].help_text = _('Please repeat your password')
        # self.fields.pop('consent_terms', None)
        # self.fields.pop('newsletter_subscription', None)

    def save(self, commit=True):
        user = super().save(commit)

        profile = BookingUserProfile(
            first_name=self.cleaned_data['first_name'],
            last_name=self.cleaned_data['last_name'],
            consent_terms=self.cleaned_data['consent_terms'],
            newsletter_subscription=self.cleaned_data['newsletter_subscription'],
            # consent_terms=self.cleaned_data['consent_terms'],
            # newsletter_subscription=self.cleaned_data['newsletter_subscription'],
            user=user,
        )
        if commit:
            profile.save()

        return user

    # def __repr__(self):
    #     return f"{self.first_name.widget}"

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
            # 'consent_terms': forms.BooleanField(attrs={'class': 'form-control'}),
            # 'newsletter_subscription': forms.BooleanField(attrs={'class': 'form-control'}),
        }

    #
    #
    #
    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     # Exclude the 'consent_terms' and 'newsletter_subscription' fields
    #     self.fields.pop('consent_terms', None)
    #     self.fields.pop('newsletter_subscription', None)
