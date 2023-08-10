from django.contrib.auth import views as auth_views, login
from django.urls import reverse_lazy
from django.views import generic as views
from coach_me.accounts.forms import LoginUserForm, RegisterUserForm
from coach_me.profiles.models import Company
from coach_me.bookings.mixins import AnonymousRequiredMixin
import logging

logger = logging.getLogger(__name__)


class RegisterUserView(AnonymousRequiredMixin, views.CreateView):
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
            error_message = """
                    We can't find your company domain in our database! 
                    Please contact our team for support or check if the corporate email address is correct!
                    """
            logger.warning(f"User registration error: {error_message}")
            form.add_error(None, error_message)
            return self.form_invalid(form)

        result = super().form_valid(form)
        login(self.request, self.object)
        logger.info(f"User registration: {object}")
        return result


class LoginUserView(auth_views.LoginView):
    template_name = 'accounts/login.html'
    form_class = LoginUserForm
    success_url = reverse_lazy('dashboard')

    def form_invalid(self, form):
        logger.warning("User login failed: Invalid credentials")
        return super().form_invalid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        placeholders = {
            'username': 'Enter your corporate email',
            'password': 'Password',
        }
        context['placeholders'] = placeholders
        return context


class LogoutUserView(auth_views.LogoutView):
    def logout(self, request):
        logger.info(f"User logged out: {request.user}")
        return super().logout(request)
