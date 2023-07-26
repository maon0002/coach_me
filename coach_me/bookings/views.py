from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.forms import modelform_factory
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy, reverse
from django.views import generic as views
from django.views.generic import DeleteView, CreateView, UpdateView
from coach_me.accounts.models import Company
from coach_me.bookings.forms import BookingForm, BookingCreateForm, BookingDetailsForm, BookingUpdateForm
from coach_me.bookings.models import Booking, Training, Lector
from coach_me.profiles.models import BookingUserProfile
from coach_me.bookings.mixins import DisabledFormFieldsMixin

# from django.http import HttpResponseRedirect

UserModel = get_user_model()


class BookingCreateView(views.CreateView):
    model = Booking
    form_class = BookingCreateForm
    template_name = 'bookings/create-booking.html'
    success_url = reverse_lazy('dashboard')

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        user = self.request.user

        # Set 'employee' and 'corporate_email' initial values from BookingUser
        form.fields['employee'].initial = user
        form.fields['corporate_email'].initial = user.email

        # Try to get the related BookingUserProfile instance
        booking_user_profile = BookingUserProfile.objects.filter(pk=user.pk).first()

        # Set 'first_name' and 'last_name' initial values from BookingUserProfile
        if booking_user_profile:
            form.fields['first_name'].initial = str(booking_user_profile.first_name)
            form.fields['last_name'].initial = str(booking_user_profile.last_name)

        # Disable the fields
        # form.fields['employee'].widget.attrs['disabled'] = True
        form.fields['employee'].widget.attrs['readonly'] = True
        form.fields['corporate_email'].widget.attrs['readonly'] = True
        form.fields['first_name'].widget.attrs['readonly'] = True
        form.fields['last_name'].widget.attrs['readonly'] = True

        # Remove the fields from the form's required fields to prevent validation errors
        for field_name in ['employee', 'corporate_email', 'first_name', 'last_name']:
            if field_name in form.fields:
                form.fields[field_name].required = False

        return form

    def form_valid(self, form):
        # Check if the booking being edited has changes in the employee or start time
        if form.instance.pk is not None:
            original_booking = Booking.objects.get(pk=form.instance.pk)
            if (
                    form.instance.employee == original_booking.employee
                    and form.instance.start_time == original_booking.start_time
            ):
                return super().form_valid(form)

        # Check if the start_time exists for the employee
        employee_availability_duplicate = Booking.objects.filter(
            employee=form.instance.employee,
            start_date=form.instance.start_date,
            start_time=form.instance.start_time,
        ).exists()

        if employee_availability_duplicate:
            form.add_error(None, "This start time is already booked for the employee.")
            return self.form_invalid(form)

        # Check if the start_time exists for the lector
        lector_availability_duplicate = Booking.objects.filter(
            lector=form.instance.lector,
            start_date=form.instance.start_date,
            start_time=form.instance.start_time,
        ).exists()

        if lector_availability_duplicate:
            form.add_error(None, "This start time is already booked for this lector.")
            return self.form_invalid(form)

        # Check if the selected lector has the selected booking_type (Training)
        lector = form.cleaned_data.get('lector')
        booking_type = form.cleaned_data.get('booking_type')

        if lector and booking_type:
            if booking_type in lector.service_integrity.all():
                return super().form_valid(form)
            else:
                form.add_error('booking_type', "The selected lector does not have the selected booking type.")
                return self.form_invalid(form)

        # Check if the employee corporate email has the correct domain name suffix
        existing_domains = Company.objects.filter(
            company_domain__iendswith=str(form.instance.employee.email).split('@')[1]
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

        return super().form_valid(form)

    def get_success_url(self):

        # Redirect to the 'dashboard' URL with the logged-in user's 'pk' as an argument
        return reverse('dashboard', kwargs={'pk': self.request.user.pk})


###OLD but gold / working
# class BookingDetailsView(views.DetailView):
#     # model = BookingUserProfile
#     model = Booking
#     template_name = 'bookings/details-booking.html'
#
#     form_class = BookingDetailsForm
#
#     def get_context_data(self, **kwargs):
#         # custom_display_names = {
#         #     'first_name': 'First Name',
#         #     'last_name': 'Last Name',
#         #     # Add more custom display names for other fields if needed
#         # }
#         context = super().get_context_data(**kwargs)
#         profile = context['object']
#         fields = [(field.name, getattr(profile, field.name)) for field in profile._meta.fields if
#                   field.name not in ['user', 'consent_terms', 'newsletter_subscription', 'picture']]
#         fields_replace_underscores = tuple([str(field[0]).replace("_", " "), str(field[1])] for field in fields)
#         context['fields'] = fields_replace_underscores
#         return context


class BookingDetailsView(views.DetailView):
    model = Booking
    template_name = 'bookings/details-booking.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        training = context['object'].booking_type
        lector = context['object'].lector

        # Retrieve the user profile for the current user
        try:
            profile = BookingUserProfile.objects.get(pk=user.pk)
        except BookingUserProfile.DoesNotExist:
            profile = None

        # Add the related BookingUserProfile to the context
        context['profile'] = profile
        context['lector'] = lector
        context['training'] = training

        return context


class BookingDeleteView(views.DeleteView):
    model = Booking
    template_name = 'bookings/delete-booking.html'

    def get_success_url(self):
        # Get the 'pk' of the logged-in user and construct the URL for the dashboard view
        logged_in_user_pk = self.request.user.pk
        return reverse_lazy('dashboard', kwargs={'pk': logged_in_user_pk})


from django.shortcuts import get_object_or_404


class BookingUpdateView(views.UpdateView):
    model = Booking
    # form_class = BookingForm
    form_class = BookingUpdateForm
    template_name = 'bookings/edit-booking.html'
    success_url = reverse_lazy('dashboard')

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields['employee'].disabled = True
        return form

    def get_initial(self):
        initial = super().get_initial()
        initial['employee'] = self.object.employee
        user = self.request.user

        try:
            profile = BookingUserProfile.objects.get(pk=user.pk)
        except BookingUserProfile.DoesNotExist:
            profile = None

        try:
            company = Company.objects.get(company_domain__iendswith=user.email.split('@')[1])
        except BookingUserProfile.DoesNotExist:
            company = None

        initial['first_name'] = profile.first_name
        initial['last_name'] = profile.first_name
        initial['corporate_email'] = user.email
        initial['company_name'] = company.short_company_name
        initial['private_email'] = profile.private_email

        # if profile.private_email:
        #     initial['private_email'] = profile.private_email
        # else:
        #     initial['private_email'] = None

        return initial

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        training = context['object'].booking_type
        lector = context['object'].lector

        # Retrieve the user profile for the current user
        try:
            profile = BookingUserProfile.objects.get(pk=user.pk)
        except BookingUserProfile.DoesNotExist:
            profile = None

        # Add the related BookingUserProfile to the context
        context['profile'] = profile
        context['lector'] = lector
        context['training'] = training

        return context

    def form_valid(self, form):
        # Check if the start_time exists for the employee
        employee_availability_duplicate = Booking.objects.filter(
            employee=form.instance.employee,
            start_date=form.instance.start_date,
            start_time=form.instance.start_time,
        ).exclude(pk=form.instance.pk).exists()

        if employee_availability_duplicate:
            form.add_error(None, "This start time is already booked for the employee.")
            return self.form_invalid(form)

        # Check if the start_time exists for the lector
        lector_availability_duplicate = Booking.objects.filter(
            lector=form.instance.lector,
            start_date=form.instance.start_date,
            start_time=form.instance.start_time,
        ).exclude(pk=form.instance.pk).exists()

        if lector_availability_duplicate:
            form.add_error(None, "This start time is already booked for this lector.")
            return self.form_invalid(form)

        # Check if the selected lector has the selected booking_type (Training)
        lector = form.cleaned_data.get('lector')
        booking_type = form.cleaned_data.get('booking_type')

        if lector and booking_type:
            if booking_type not in lector.service_integrity.all():
                form.add_error('booking_type', "The selected lector does not have the selected booking type.")
                return self.form_invalid(form)

        # Check if the employee corporate email has the correct domain name suffix
        existing_domains = Company.objects.filter(
            company_domain__iendswith=str(form.instance.employee.email).split('@')[1]
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

        # Save the form and update the booking
        return super().form_valid(form)

    def get_success_url(self):
        # Redirect to the dashboard page
        return reverse_lazy('dashboard', kwargs={'pk': self.request.user.pk})

    def post(self, request, *args, **kwargs):
        # Check if the cancel button is pressed
        if "cancel" in request.POST:
            return HttpResponseRedirect(self.get_success_url())
        return super().post(request, *args, **kwargs)


#
# class BookingUpdateView(views.UpdateView):
#     model = Booking
#     # form_class = BookingForm
#     form_class = BookingUpdateForm
#     template_name = 'bookings/edit-booking.html'
#     success_url = reverse_lazy('dashboard')
#
#     def get_form(self, form_class=None):
#         form = super().get_form(form_class)
#         form.fields['employee'].disabled = True
#         return form
#
#     def get_initial(self):
#         initial = super().get_initial()
#         initial['employee'] = self.object.employee
#         user = self.request.user
#
#         try:
#             profile = BookingUserProfile.objects.get(pk=user.pk)
#         except BookingUserProfile.DoesNotExist:
#             profile = None
#
#         try:
#             company = Company.objects.get(company_domain__iendswith=user.email.split('@')[1])
#         except BookingUserProfile.DoesNotExist:
#             company = None
#
#         initial['first_name'] = profile.first_name
#         initial['last_name'] = profile.first_name
#         initial['corporate_email'] = user.email
#         initial['company_name'] = company.short_company_name
#         initial['private_email'] = profile.private_email
#
#         # if profile.private_email:
#         #     initial['private_email'] = profile.private_email
#         # else:
#         #     initial['private_email'] = None
#
#         return initial
#
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         user = self.request.user
#         training = context['object'].booking_type
#         lector = context['object'].lector
#
#         # Retrieve the user profile for the current user
#         try:
#             profile = BookingUserProfile.objects.get(pk=user.pk)
#         except BookingUserProfile.DoesNotExist:
#             profile = None
#
#         # Add the related BookingUserProfile to the context
#         context['profile'] = profile
#         context['lector'] = lector
#         context['training'] = training
#
#         return context
#
#     def form_valid(self, form):
#         # Check if the booking being edited has changes in the employee or start time
#         if form.instance.pk is not None:
#             original_booking = Booking.objects.get(pk=form.instance.pk)
#             if (
#                     form.instance.employee == original_booking.employee
#                     and form.instance.start_time == original_booking.start_time
#             ):
#                 return super().form_valid(form)
#
#         # Check if the start_time exists for the employee
#         employee_availability_duplicate = Booking.objects.filter(
#             employee=form.instance.employee,
#             start_date=form.instance.start_date,
#             start_time=form.instance.start_time,
#         ).exists()
#
#         if employee_availability_duplicate:
#             form.add_error(None, "This start time is already booked for the employee.")
#             return self.form_invalid(form)
#
#         # Check if the start_time exists for the lector
#         lector_availability_duplicate = Booking.objects.filter(
#             lector=form.instance.lector,
#             start_date=form.instance.start_date,
#             start_time=form.instance.start_time,
#         ).exists()
#
#         if lector_availability_duplicate:
#             form.add_error(None, "This start time is already booked for this lector.")
#             return self.form_invalid(form)
#
#         # Check if the selected lector has the selected booking_type (Training)
#         lector = form.cleaned_data.get('lector')
#         booking_type = form.cleaned_data.get('booking_type')
#
#         if lector and booking_type:
#             if booking_type in lector.service_integrity.all():
#                 return super().form_valid(form)
#             else:
#                 form.add_error('booking_type', "The selected lector does not have the selected booking type.")
#                 return self.form_invalid(form)
#
#         # Check if the employee corporate email has the correct domain name suffix
#         existing_domains = Company.objects.filter(
#             company_domain__iendswith=str(form.instance.employee.email).split('@')[1]
#         ).exists()
#
#         if not existing_domains:
#             form.add_error(
#                 None,
#                 """
#                 We can't find your company domain in our database!
#                 Please contact our team for support or check if the corporate email address is correct!
#                 """
#             )
#             return self.form_invalid(form)
#
#         return super().form_valid(form)
#
#     def get_success_url(self):
#         # Get the 'pk' of the logged-in user and construct the URL for the dashboard view
#         logged_in_user_pk = self.request.user.pk
#         return reverse_lazy('dashboard', kwargs={'pk': logged_in_user_pk})


class IndexView(views.ListView):
    model = Training
    template_name = 'index.html'


class TrainingListView(views.ListView):
    model = Training
    template_name = 'bookings/trainings.html'


class LectorListView(views.ListView):
    model = Lector
    template_name = 'bookings/lectors.html'


class TrainingCreateView(views.CreateView):
    model = Booking
    template_name = 'trainings/create-training.html'
    fields = '__all__'
    success_url = reverse_lazy('add training')


class TrainingDetailsView(views.DetailView):
    model = Training
    template_name = 'trainings/details-training.html'


class TrainingUpdateView(views.UpdateView):
    model = Training
    template_name = 'trainings/edit-training.html'
    fields = '__all__'

    def get_success_url(self):
        return reverse_lazy('details training', kwargs={'pk': self.object.pk})


class TrainingDeleteView(DisabledFormFieldsMixin, views.DeleteView):
    model = Training
    template_name = 'trainings/delete-training.html'
    form_class = modelform_factory(
        Booking,
        fields='__all__'
    )

    def get_form_kwargs(self):
        instance = self.get_object()
        form_kwargs = super().get_form_kwargs()

        form_kwargs.update(instance=instance)
        return form_kwargs
