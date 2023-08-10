from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model

from coach_me.accounts.forms import RegisterUserForm, LoginUserForm
from coach_me.profiles.models import Company

User = get_user_model()


class AccountsViewTests(TestCase):

    def setUp(self):
        self.client = Client()

    def test_register_view(self):
        response = self.client.get(reverse('register_user'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts/register.html')
        self.assertIsInstance(response.context['form'], RegisterUserForm)

    def test_valid_registration(self):
        company = Company.objects.create(company_domain='example.com')
        response = self.client.post(reverse('register_user'), {
            'first_name': 'John',
            'last_name': 'Doe',
            'email': 'john.doe@example.com',
            'password1': 'strongpassword',
            'password2': 'strongpassword',
        })
        self.assertEqual(response.status_code, 302)  # Should redirect after successful registration
        self.assertTrue(User.objects.filter(email='john.doe@example.com').exists())

    def test_invalid_registration(self):
        response = self.client.post(reverse('register_user'), {
            'first_name': 'John',
            'last_name': 'Doe',
            'email': 'john.doe@example.com',
            'password1': 'password1',
            'password2': 'password2',
        })
        self.assertEqual(response.status_code, 200)
        self.assertFormError(response, 'form', 'password2', "The two password fields didn't match.")

    def test_login_view(self):
        response = self.client.get(reverse('login_user'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts/login.html')
        self.assertIsInstance(response.context['form'], LoginUserForm)

    def test_valid_login(self):
        user = User.objects.create_user(email='john.doe@example.com', password='strongpassword')
        response = self.client.post(reverse('login_user'), {
            'username': 'john.doe@example.com',
            'password': 'strongpassword',
        })
        self.assertEqual(response.status_code, 302)  # Should redirect after successful login

    def test_invalid_login(self):
        response = self.client.post(reverse('login_user'), {
            'username': 'john.doe@example.com',
            'password': 'wrongpassword',
        })
        self.assertEqual(response.status_code, 200)
        self.assertFormError(response, 'form', None, 'Please enter a correct corporate email and password.')

    def test_logout_view(self):
        response = self.client.get(reverse('logout_user'))
        self.assertEqual(response.status_code, 302)  # Should redirect after logout
