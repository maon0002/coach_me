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
from django.core.paginator import Paginator
import csv
from django.http import HttpResponse

UserModel = get_user_model()


def export_csv(request):
    response = HttpResponse(content_type='text/csv')
    writer = csv.writer(response)

    # Fetch the data and write to CSV
    user = request.user
    if user.c_labels == 'COACHME_STAFF':
        queryset = Booking.objects.all()
        response['Content-Disposition'] = 'attachment; filename="staff_all_scheduled_trainings.csv"'
    elif user.c_labels == 'COACHME_USER':
        queryset = Booking.objects.filter(employee=user).all()
        response['Content-Disposition'] = 'attachment; filename="my_bookings.csv"'
    elif user.c_labels == 'COACHME_LECTOR':
        lector = Lector.objects.filter(user_id=user.pk).get()
        queryset = Booking.objects.filter(lector=lector).order_by('-start_date').all()
        response['Content-Disposition'] = 'attachment; filename="lector_scheduled_trainings.csv"'
    else:
        queryset = None
        response['Content-Disposition'] = 'attachment; filename="no_data.csv"'

    try:
        fields = [field.name for field in queryset.model._meta.fields]
    except AttributeError:
        return redirect(reverse_lazy('dashboard', kwargs={'pk': user.pk}))

    # Write the headers
    writer.writerow(fields)

    # Write the data
    for item in queryset:
        row = [getattr(item, field) for field in fields]
        writer.writerow(row)

    return response


class DashboardView(LoginRequiredMixin, views.ListView):
    model = Booking
    template_name = 'dashboard.html'
    context_object_name = 'bookings'
    paginate_by = 10  # TODO not working properly

    def get_queryset(self):
        user = self.request.user
        booking_user = BookingUserProfile.objects.filter(pk=user.pk).get()
        if user.c_labels == 'COACHME_STAFF':
            bookings = Booking.objects.order_by('start_date').all()
            return bookings
        elif user.c_labels == 'COACHME_USER':
            bookings = Booking.objects.filter(employee=user).order_by('start_date').all()
            return bookings
        elif user.c_labels == 'COACHME_LECTOR':
            lector = Lector.objects.filter(user_id=user.pk).get()
            bookings = Booking.objects.filter(lector_id=lector.pk).order_by('start_date').all()
            return bookings

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        current_date = timezone.now().date()
        # GET all existed bookings for a staff user
        if user.c_labels == 'COACHME_STAFF':
            past_bookings = Booking.objects.filter(
                start_date__lt=current_date
            ).order_by('-start_date').all()
            future_bookings = Booking.objects.filter(
                start_date__gte=current_date
            ).order_by('start_date').all()

        # GET all existed bookings with the current user as a lector
        elif user.c_labels == 'COACHME_LECTOR':
            lector = Lector.objects.filter(user_id=user.pk).get()

            past_bookings = Booking.objects.filter(
                lector=lector,
                start_date__lt=current_date
            ).order_by('-start_date').all()

            future_bookings = Booking.objects.filter(
                lector=lector,
                start_date__gte=current_date
            ).order_by('start_date').all()

            context['lector'] = lector

        # GET all existed bookings for the current user
        else:
            past_bookings = Booking.objects.filter(
                employee=user,
                start_date__lt=current_date
            ).order_by('-start_date').all()
            future_bookings = Booking.objects.filter(
                employee=user,
                start_date__gte=current_date
            ).order_by('start_date').all()

        context['past_bookings_count'] = len(past_bookings)
        context['future_bookings_count'] = len(future_bookings)

        paginator_past = Paginator(past_bookings, self.paginate_by)
        paginator_future = Paginator(future_bookings, self.paginate_by)

        page_number_past = self.request.GET.get('past_page')
        page_number_future = self.request.GET.get('future_page')

        past_bookings = paginator_past.get_page(page_number_past)
        future_bookings = paginator_future.get_page(page_number_future)

        context['past_bookings'] = past_bookings
        context['future_bookings'] = future_bookings

        # Retrieve the user profile for the current user
        try:
            profile = BookingUserProfile.objects.get(pk=user.pk)

        except BookingUserProfile.DoesNotExist:
            profile = None

        # Add the related BookingUserProfile to the context
        context['profile'] = profile

        return context


class ProfileDetailsView(LoginRequiredMixin, UserPassesTestMixin, views.DetailView):
    model = BookingUserProfile
    template_name = 'profiles/details-profile.html'
    form_class = ProfileDetailsForm

    def get_context_data(self, **kwargs):
        user = self.request.user
        booking_user = BookingUserProfile.objects.filter(pk=user.pk).get()
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
                      'company',
                  ]
                  ]
        fields_replace_underscores = list([str(field[0]).replace("_", " "), str(field[1])] for field in fields)

        company_name = Company.objects.get(
            company_domain__iendswith=user.email.split('@')[1]
        ).short_company_name

        if not booking_user.is_lector:
            bookings_count = Booking.objects.filter(employee=user).count()
            active_bookings_count = Booking.objects.filter(
                employee=user,
                start_date__gte=current_date,
            ).count()
            past_booking_count = bookings_count - active_bookings_count
        else:
            lector = Lector.objects.filter(user_id=user.pk).get()
            bookings_count = Booking.objects.filter(lector=lector).count()
            active_bookings_count = Booking.objects.filter(
                lector=lector,
                start_date__gte=current_date,
            ).count()
            past_booking_count = bookings_count - active_bookings_count

        context.update({'company': company_name})
        # context['company'] = company_name
        context['fields'] = fields_replace_underscores
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

        # Try to get the related BookingUserProfile instance
        try:
            booking_user_profile = BookingUserProfile.objects.filter(pk=user.pk).get()
        except BookingUserProfile.DoesNotExist:
            booking_user_profile = None

        # Set 'first_name' and 'last_name' initial values from BookingUserProfile
        form.fields['first_name'].initial = str(booking_user_profile.first_name)
        form.fields['last_name'].initial = str(booking_user_profile.last_name)

        # Remove the fields from the form's required fields to prevent validation errors
        for field_name in [
            # 'company',
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
            form.fields[field_name].widget.attrs['disabled'] = True
        return form
