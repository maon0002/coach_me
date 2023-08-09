from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from coach_me.profiles.models import BookingUserProfile, Company
from coach_me.bookings.models import Booking
from coach_me.profiles.views import ProfileDetailsView


class ProfileDetailsViewTest(TestCase):
    def setUp(self):
        # Set up your test data here
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser', email='testuser@example.com', password='testpass'
        )
        self.profile = BookingUserProfile.objects.create(user=self.user)
        self.company = Company.objects.create(
            company_domain='example.com', short_company_name='Test Company'
        )
        self.booking1 = Booking.objects.create(employee=self.user)
        self.booking2 = Booking.objects.create(employee=self.user)


    def test_profile_details_view(self):
        # Log in as the user
        self.client.login(username='testuser', password='testpass')

        # Send a GET request to the profile details view
        response = self.client.get(reverse('details profile', args=[self.profile.pk]))

        # Check that the response has a successful status code
        self.assertEqual(response.status_code, 200)

        # Check that the user's profile data is present in the response context
        self.assertEqual(response.context['object'], self.profile)
        self.assertContains(response, self.profile.first_name)
        # Add more assertions for other profile fields
