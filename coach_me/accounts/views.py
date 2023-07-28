from django import forms
from django.contrib.auth import views as auth_views, login, get_user_model
from django.contrib.auth import mixins as auth_mixins
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.views import generic as views
from coach_me.accounts.forms import LoginUserForm, RegisterUserForm
from coach_me.profiles.models import Company


# class RegisterUserView(views.CreateView):
#     template_name = 'accounts/register.html'
#     form_class = RegisterUserForm
#     success_url = reverse_lazy('index')
#
#     # Static way of providing `success_url`
#     # success_url = reverse_lazy('register_user')
#
#     def form_valid(self, form):
#         result = super().form_valid(form)
#         login(self.request, self.object)
#
#         return result
#
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         placeholders = {
#             'first_name': 'First name',
#             'last_name': 'Last name',
#             'email': 'Enter your corporate email',
#             'password1': 'Password',
#             'password2': 'Repeat password',
#         }
#         context['placeholders'] = placeholders
#         return context


# class RegisterUserView(views.CreateView):
#     template_name = 'accounts/register.html'
#     form_class = RegisterUserForm
#     success_url = reverse_lazy('index')
#
#     # Static way of providing `success_url`
#     # success_url = reverse_lazy('register_user')
#
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         placeholders = {
#             'first_name': 'First name',
#             'last_name': 'Last name',
#             'email': 'Enter your corporate email',
#             'password1': 'Password',
#             'password2': 'Repeat password',
#         }
#         context['placeholders'] = placeholders
#         return context
#
#     def form_valid(self, form):
#         result = super().form_valid(form)
#         login(self.request, self.object)
#         return result

# TODO add OnlyAnonymousMixin 
class OnlyAnonymousMixin:
    pass


class RegisterUserView(OnlyAnonymousMixin, views.CreateView):
    template_name = 'accounts/register.html'
    form_class = RegisterUserForm
    success_url = reverse_lazy('index')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        placeholders = {
            'first_name': 'First name',
            'last_name': 'Last name',
            'email': 'Enter your corporate email',
            'password1': 'Password',
            'password2': 'Repeat password',
        }
        context['placeholders'] = placeholders
        return context

    def form_valid(self, form):
        # Check if the employee corporate email has the correct domain name suffix
        existing_domains = Company.objects.filter(
            company_domain__iendswith=str(form.instance.email).split('@')[1]
        ).exists()

        if not existing_domains:
            form.add_error(
                None,
                """
                We can't find your company domain in our database! 
                Please contact our team for support or check if the corporate email address is correct!
                """
            )
            return self.form_invalid(form)

        result = super().form_valid(form)
        login(self.request, self.object)
        return result


class LoginUserView(auth_views.LoginView):
    template_name = 'accounts/login.html'
    # authentication_form = LoginUserForm
    form_class = LoginUserForm
    success_url = reverse_lazy('dashboard')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        placeholders = {
            'username': 'Enter your corporate email',
            'password': 'Password',
        }
        context['placeholders'] = placeholders
        return context


class LogoutUserView(auth_views.LogoutView):
    pass
