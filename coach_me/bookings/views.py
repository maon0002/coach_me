from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy, reverse
from django.utils import timezone
from django.views import generic as views
from coach_me.bookings.forms import BookingCreateForm, BookingUpdateForm
from coach_me.bookings.models import Booking
from coach_me.lectors.models import Lector
from coach_me.profiles.models import BookingUserProfile, Company
from django.http import HttpResponseRedirect
from coach_me.bookings.mixins import DefineModelsMixin
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from coach_me.trainings.models import Training
import logging

logger = logging.getLogger(__name__)
UserModel = get_user_model()




class IndexView(DefineModelsMixin, views.ListView):
    model = Training
    template_name = 'index.html'

    # @method_decorator(cache_page(1))  # Cache will expire in 1 hour (3600 seconds)
    # def dispatch(self, *args, **kwargs):
    #     return super().dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Retrieve the BookingUserProfile and add it to the context

        user = self.get_booking_user()
        booking_user_profile = self.get_booking_user_profile()

        if user and booking_user_profile:
            context['user'] = self.get_booking_user().get()

            # print(user.is_staff, "<<<<<<< USER is staff?")
            context['booking_user_profile'] = self.get_booking_user_profile().get()

            # print(booking_user_profile.is_lector, "<<<<<<< BUP is Lector?")
            return context

        else:
            context = super().get_context_data(**kwargs)
        return context


class BookingCreateView(LoginRequiredMixin, views.CreateView):
    model = Booking
    form_class = BookingCreateForm
    template_name = 'bookings/create-booking.html'
    success_url = reverse_lazy('dashboard')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        trainings = Training.objects.all()
        lectors = Lector.objects.all()

        training_lectors_dictionary = {}

        for training in trainings:
            # Filter lectors based on the service_integrity relationship
            available_lectors = DefineModelsMixin.get_lectors_by_training(training, list_csv=True)
            training_lectors_dictionary[training] = available_lectors

        context['trainings'] = trainings
        context['lectors'] = lectors
        context['objects_dict'] = training_lectors_dictionary

        return context

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        user = self.request.user
        booking_user_profile = BookingUserProfile.objects.filter(pk=user.pk).get()

        # # TODO check the logic for lector to booked for another person and remove the IF if not needed
        # if booking_user_profile and not booking_user_profile.is_lector:

        # Set 'employee' and 'corporate_email' initial values from BookingUser
        form.fields['employee'].initial = user
        form.fields['corporate_email'].initial = user.email

        # Set 'first_name' and 'last_name' initial values from BookingUserProfile
        # if booking_user_profile:
        form.fields['first_name'].initial = booking_user_profile.first_name
        form.fields['last_name'].initial = booking_user_profile.last_name

        # Set 'corporate_email' initial value from User
        form.fields['corporate_email'].initial = user.email

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

        # Get the selected training slug from the query parameter
        selected_training_slug = self.request.GET.get('training')

        if selected_training_slug:
            try:
                selected_training = Training.objects.get(slug=selected_training_slug)
                # Set the selected training as the initial value for the training field
                form.fields['booking_type'].initial = selected_training
            except Training.DoesNotExist:
                pass

        return form
        # return form

    def form_valid(self, form):
        # Check if the booking being edited has changes in the employee or start time
        if form.instance.pk is not None:
            original_booking = Booking.objects.get(pk=form.instance.pk)
            if not (
                    form.instance.employee == original_booking.employee
                    and form.instance.start_time == original_booking.start_time
            ):
                return self.form_invalid(form)

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
                form.add_error(
                    'booking_type',
                    "The selected lector does not have the selected booking type.")
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
                Please contact our team for support or check if the corporate email address 
                is correct!
                """
            )
            return self.form_invalid(form)
        logger.info(
            f"""User: {self.request.user} from company : {existing_domains}
            create booking 
            for Training: {booking_type} 
            with Lector: {lector}"""
        )

        return super().form_valid(form)

    def get_success_url(self):

        # Redirect to the 'dashboard' URL with the logged-in user's 'pk' as an argument
        return reverse('dashboard', kwargs={'pk': self.request.user.pk})


class BookingDetailsView(LoginRequiredMixin, views.DetailView):
    model = Booking
    template_name = 'bookings/details-booking.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        training = context['object'].booking_type
        lector = context['object'].lector
        current_date = timezone.now().date()

        current_booking = Booking.objects.filter(pk=context['object'].pk).get()
        # current_booking = get_object_or_404(Booking, pk=self.kwargs['pk'])

        # Retrieve the user profile for the current user
        try:
            profile = BookingUserProfile.objects.filter(pk=current_booking.employee_id).get()
        except BookingUserProfile.DoesNotExist:
            profile = None

        profile_lector = BookingUserProfile.objects.get(pk=user.pk)

        company = Company.objects.filter(company_domain__iendswith=user.email.split('@')[1]).get()

        # Add the related BookingUserProfile to the context
        context['profile'] = profile
        context['profile_lector'] = profile_lector
        context['lector'] = lector
        context['training'] = training
        context['company'] = company
        context['current_date'] = current_date

        return context


class BookingDeleteView(LoginRequiredMixin, views.DeleteView):
    model = Booking
    template_name = 'bookings/delete-booking.html'

    def get_success_url(self):
        # Get the 'pk' of the logged-in user and construct the URL for the dashboard view
        logged_in_user_pk = self.request.user.pk
        return reverse_lazy('dashboard', kwargs={'pk': logged_in_user_pk})


class BookingUpdateView(LoginRequiredMixin, views.UpdateView):
    model = Booking
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
