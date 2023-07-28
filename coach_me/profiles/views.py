from django.conf.urls.static import static
from django.contrib.auth import get_user_model
from django.forms import modelform_factory
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import DetailView, ListView

from coach_me.accounts.models import BookingUser
from coach_me.bookings.mixins import DisabledFormFieldsMixin
from coach_me.bookings.models import Booking
from coach_me.profiles.forms import ProfileUpdateForm, ProfileDeleteForm, ProfileDetailsForm
from coach_me.profiles.models import BookingUserProfile, Company
from django.views import generic as views, View

UserModel = get_user_model()


class DashboardView(ListView):
    model = Booking  # or def get_queryset изобщо няма да гледа модела
    template_name = 'dashboard.html'  # Use the template name where you want to display the bookings
    context_object_name = 'bookings'  # Name of the context variable to be used in the template
    paginate_by = 10  # Optional: Set the number of bookings to be displayed per page

    def get_queryset(self):
        user = self.request.user
        return Booking.objects.filter(employee=user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user

        # Retrieve the user profile for the current user
        try:
            profile = BookingUserProfile.objects.get(pk=user.pk)
        except BookingUserProfile.DoesNotExist:
            profile = None

        # Add the related BookingUserProfile to the context
        context['profile'] = profile

        # #TODO _set from the bookings because of the employee in the Booking model fk
        context['bookingsss'] = user.booking_set.all()
        # bookings_count = Booking.objects.count()
        # context['bookings_count'] = bookings_count

        return context


class ProfileDetailsView(DetailView):
    model = BookingUserProfile
    template_name = 'profiles/details-profile.html'
    form_class = ProfileDetailsForm

    def get_context_data(self, **kwargs):
        user = self.request.user
        custom_display_names = {
            'first_name': 'First Name',
            'last_name': 'Last Name',
            # Add more custom display names for other fields if needed
        }
        context = super().get_context_data(**kwargs)
        profile = context['object']
        fields = [(field.name, getattr(profile, field.name)) for field in profile._meta.fields if
                  # field.name not in ['user', 'consent_terms', 'newsletter_subscription', 'picture']]
                  field.name not in ['user', 'consent_terms', 'newsletter_subscription', 'picture']]
        # print(fields)
        # fields2 = list([[str(field[0]).replace("_", " "), field[1]] for field in fields])
        fields_replace_underscores = tuple([str(field[0]).replace("_", " "), str(field[1])] for field in fields)
        # print(fields_replace_underscores)
        context['fields'] = fields_replace_underscores
        context['custom_display_names'] = custom_display_names  # Pass the dictionary to the template

        # TODO _set from the bookings because of the employee in the Booking model fk
        context['bookingsss'] = user.booking_set.all()
        # bookings_count = Booking.objects.count()
        bookings_count = Booking.objects.filter(employee=user).count()
        context['bookings_count'] = bookings_count

        return context


class ProfileUpdateView(views.UpdateView):
    model = BookingUserProfile
    template_name = 'profiles/edit-profile.html'
    form_class = ProfileUpdateForm

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        user = self.request.user

        try:
            company = Company.objects.get(company_domain__iendswith=user.email.split('@')[1])
        except Company.DoesNotExist:
            company = None

        # Set 'employee' and 'corporate_email' initial values from BookingUser
        if company.short_company_name:
            form.fields['company'].initial = company.short_company_name
        else:
            form.fields['company'].initial = None
            # form.fields['corporate_email'].initial = user.email

        # Try to get the related BookingUserProfile instance
        booking_user_profile = BookingUserProfile.objects.filter(pk=user.pk).first()

        # Set 'first_name' and 'last_name' initial values from BookingUserProfile
        if booking_user_profile:
            form.fields['first_name'].initial = str(booking_user_profile.first_name)
            form.fields['last_name'].initial = str(booking_user_profile.last_name)

        # Disable the fields
        # form.fields['corporate_email'].widget.attrs['readonly'] = True
        # form.fields['first_name'].widget.attrs['readonly'] = True
        # form.fields['last_name'].widget.attrs['readonly'] = True

        # Remove the fields from the form's required fields to prevent validation errors
        for field_name in [
            # 'corporate_email',
            'picture',
            'first_name', 'last_name', ]:
            if field_name in form.fields:
                form.fields[field_name].required = False

        return form

    def get_success_url(self):
        return reverse_lazy('details profile', kwargs={'pk': self.object.pk})


class ProfileDeleteView(View):
    template_name = 'profiles/delete-profile.html'
    success_url = reverse_lazy('index')

    def get(self, request, pk):
        profile = get_object_or_404(BookingUserProfile, pk=pk)
        user = get_object_or_404(BookingUser, pk=pk)
        return render(request, self.template_name,
                      {
                          'profile': profile,
                          'user': user,

                      }
                      )

    def post(self, request, pk):
        profile = get_object_or_404(BookingUserProfile, pk=pk)
        user = get_object_or_404(BookingUser, pk=pk)
        profile.delete()
        user.delete()

        return redirect(self.success_url)
