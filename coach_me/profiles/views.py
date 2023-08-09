from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin, IsStaffdMixin
from django.contrib.auth.mixins import UserPassesTestMixin
from django.shortcuts import redirect
from django.urls import reverse_lazy
from coach_me.bookings.models import Booking
from coach_me.lectors.models import Lector
from coach_me.profiles.forms import ProfileUpdateForm, ProfileDetailsForm, CompanyListForm, CompanyDetailsForm
from coach_me.profiles.models import BookingUserProfile, Company
from django.views import generic as views
from django.utils import timezone

UserModel = get_user_model()


class DashboardView(LoginRequiredMixin, views.ListView):
    model = Booking
    template_name = 'dashboard.html'
    context_object_name = 'bookings'
    paginate_by = 2  # TODO not working properly

    def get_queryset(self):
        user = self.request.user
        booking_user = BookingUserProfile.objects.filter(pk=user.pk).get()
        if not booking_user.is_lector:
            bookings = Booking.objects.filter(employee=user).order_by('start_date').all()
            return bookings
        elif booking_user.is_lector:
            lector = Lector.objects.filter(user_id=user.pk).get()
            bookings = Booking.objects.filter(lector_id=lector.pk).order_by('start_date').all()
            return bookings

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        booking_user = BookingUserProfile.objects.filter(pk=user.pk).get()
        if not booking_user.is_lector:
            current_date = timezone.now().date()

            past_bookings = Booking.objects.filter(
                employee=user,
                start_date__lt=current_date
            ).order_by('-start_date').all()
            future_bookings = Booking.objects.filter(
                employee=user,
                start_date__gte=current_date
            ).order_by('start_date').all()

            # Retrieve the user profile for the current user
            try:
                profile = BookingUserProfile.objects.get(pk=user.pk)
            except BookingUserProfile.DoesNotExist:
                profile = None

            # Add the related BookingUserProfile to the context
            context['profile'] = profile
            context['past_bookings'] = past_bookings
            context['future_bookings'] = future_bookings


        elif booking_user.is_lector:
            lector = Lector.objects.filter(user_id=user.pk).get()
            # current_booking = Booking.objects.filter(user_id=user.pk).get()
            current_date = timezone.now().date()

            past_bookings = Booking.objects.filter(
                lector=lector,
                start_date__lt=current_date
            ).order_by('-start_date').all()

            future_bookings = Booking.objects.filter(
                lector=lector,
                start_date__gte=current_date
            ).order_by('start_date').all()

            # Retrieve the user profile for the current user
            try:
                profile = BookingUserProfile.objects.get(pk=user.pk)

            except BookingUserProfile.DoesNotExist:
                profile = None

            # Add the related BookingUserProfile to the context
            context['profile'] = profile
            context['past_bookings'] = past_bookings
            context['future_bookings'] = future_bookings
            context['lector'] = lector

        return context


# class DashboardView(views.ListView):
#     model = Booking
#     template_name = 'dashboard.html'
#     context_object_name = 'bookings'
#     paginate_by = 10  # TODO not working properly
#
#     def get_queryset(self):
#         user = self.request.user
#         return Booking.objects.filter(employee=user).order_by('start_date').all()
#
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         user = self.request.user
#         current_date = timezone.now().date()
#
#         past_bookings = Booking.objects.filter(
#             employee=user,
#             start_date__lt=current_date
#         ).order_by('-start_date').all()
#         future_bookings = Booking.objects.filter(
#             employee=user,
#             start_date__gte=current_date
#         ).order_by('start_date').all()
#
#         # Retrieve the user profile for the current user
#         try:
#             profile = BookingUserProfile.objects.get(pk=user.pk)
#         except BookingUserProfile.DoesNotExist:
#             profile = None
#
#         # Add the related BookingUserProfile to the context
#         context['profile'] = profile
#         context['past_bookings'] = past_bookings
#         context['future_bookings'] = future_bookings
#
#         return context


class ProfileDetailsView(LoginRequiredMixin, UserPassesTestMixin, views.DetailView):
    model = BookingUserProfile
    template_name = 'profiles/details-profile.html'
    form_class = ProfileDetailsForm

    def get_context_data(self, **kwargs):
        user = self.request.user
        context = super().get_context_data(**kwargs)
        current_date = timezone.now().date()
        profile = context['object']
        fields = [(field.name, getattr(profile, field.name)) for field in profile._meta.fields if
                  field.name not in [
                      'user',
                      'consent_terms',
                      'newsletter_subscription',
                      'picture',
                      'is_lector',
                      'company', ]
                  ]
        fields_replace_underscores = list([str(field[0]).replace("_", " "), str(field[1])] for field in fields)

        context['fields'] = fields_replace_underscores

        company_name = Company.objects.get(
            company_domain__iendswith=user.email.split('@')[1]
        ).short_company_name

        context['company_name'] = company_name

        bookings_count = Booking.objects.filter(employee=user).count()
        active_bookings_count = Booking.objects.filter(
            employee=user,
            start_date__gte=current_date,
        ).count()
        past_booking_count = bookings_count - active_bookings_count
        context['bookings_count'] = bookings_count
        context['active_bookings_count'] = active_bookings_count
        context['past_booking_count'] = past_booking_count

        return context

    def test_func(self):
        # Ensure that only the owner of the profile can access it
        return self.request.user == self.get_object().user


class ProfileUpdateView(LoginRequiredMixin, UserPassesTestMixin, views.UpdateView):
    model = BookingUserProfile
    template_name = 'profiles/edit-profile.html'
    form_class = ProfileUpdateForm

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        user = self.request.user

        # Set 'employee' and 'corporate_email' initial values from BookingUser
        try:
            company = Company.objects.get(company_domain__iendswith=user.email.split('@')[1])
            form.fields['company'].initial = company.short_company_name
        except Company.DoesNotExist:
            company = None
            form.fields['company'].initial = None

            print(company)

        # Try to get the related BookingUserProfile instance
        try:
            booking_user_profile = BookingUserProfile.objects.filter(pk=user.pk).get()

        except BookingUserProfile.DoesNotExist:
            booking_user_profile = None

        # Set 'first_name' and 'last_name' initial values from BookingUserProfile
        # if booking_user_profile:
        form.fields['first_name'].initial = str(booking_user_profile.first_name)
        form.fields['last_name'].initial = str(booking_user_profile.last_name)

        # Remove the fields from the form's required fields to prevent validation errors
        for field_name in [
            'company',
            'picture',
            'first_name',
            'last_name',
        ]:
            if field_name in form.fields:
                form.fields[field_name].required = False

        return form

    def get_success_url(self):
        return reverse_lazy('details profile', kwargs={'pk': self.object.pk})

    def test_func(self):
        # Ensure that only the owner of the profile can access it
        return self.request.user == self.get_object().user


class ProfileDeleteView(LoginRequiredMixin, UserPassesTestMixin, views.DeleteView):
    model = BookingUserProfile
    template_name = 'profiles/delete-profile.html'
    success_url = reverse_lazy('index')

    def test_func(self):
        # Ensure that only the owner of the profile can delete it
        return self.request.user == self.get_object().user


class CompanyListView(IsStaffdMixin, views.ListView):
    # model = Training
    template_name = 'companies/companies.html'
    paginate_by = 20
    queryset = Company.objects.all().order_by('-updated_on')
    form_class = CompanyListForm

    # @method_decorator(cache_page(3600))  # Cache will expire in 1 hour (3600 seconds)
    # def dispatch(self, *args, **kwargs):
    #     return super().dispatch(*args, **kwargs)


class CompanyCreateView(IsStaffdMixin, views.CreateView):
    model = Company
    template_name = 'companies/create-company.html'
    fields = '__all__'
    success_url = reverse_lazy('companies')

    def form_valid(self, form):
        # Save the Lector instance and redirect to the success URL
        self.object = form.save()
        return redirect(self.get_success_url())


class CompanyDetailsView(IsStaffdMixin, views.DetailView):
    model = Company
    template_name = 'companies/details-company.html'
    form_class = CompanyDetailsForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        profile = context['object']
        fields = [
            (field.name, getattr(profile, field.name)) for field in profile._meta.fields
        ]
        fields_replace_underscores = list([str(field[0]).replace("_", " "), str(field[1])] for field in fields)
        context['fields'] = fields_replace_underscores

        return context


class CompanyUpdateView(IsStaffdMixin, views.UpdateView):
    model = Company
    template_name = 'companies/edit-company.html'
    fields = '__all__'

    def get_success_url(self):
        return reverse_lazy('details company', kwargs={'slug': self.object.slug})


class CompanyDeleteView(IsStaffdMixin, views.DeleteView):
    model = Company
    template_name = 'companies/delete-company.html'
    success_url = reverse_lazy('companies')

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        for field_name in form.fields:
            # form.fields[field_name].widget.attrs['readonly'] = True
            form.fields[field_name].widget.attrs['disabled'] = True
        return form
