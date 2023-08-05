from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin, IsStaffdMixin
from django.forms import modelform_factory
from django.shortcuts import redirect
from django.urls import reverse_lazy, reverse
from django.views import generic as views
from django.views.decorators.cache import cache_page
from coach_me.bookings.models import Booking, Lector
from coach_me.profiles.models import BookingUserProfile
from coach_me.trainings.models import Training
from coach_me.bookings.mixins import DisabledFormFieldsMixin, DefineModelsMixin
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page

UserModel = get_user_model()


class TrainingListView(views.ListView):
    # model = Training
    template_name = 'bookings/../../templates/trainings/trainings.html'
    paginate_by = 4
    queryset = Training.objects.all().order_by('-updated_on')

    # @method_decorator(cache_page(3600))  # Cache will expire in 1 hour (3600 seconds)
    # def dispatch(self, *args, **kwargs):
    #     return super().dispatch(*args, **kwargs)


class TrainingCreateView(LoginRequiredMixin, IsStaffdMixin, views.CreateView):
    model = Training
    template_name = 'trainings/create-training.html'
    fields = '__all__'
    success_url = reverse_lazy('trainings')

    def form_valid(self, form):
        # Save the Lector instance and redirect to the success URL
        self.object = form.save()
        return redirect(self.get_success_url())


class TrainingDetailsView(views.DetailView):
    model = Training
    template_name = 'trainings/details-training.html'

    def get_context_data(self, **kwargs):
        user = self.request.user
        context = super().get_context_data(**kwargs)
        booking_user_profile = BookingUserProfile.objects.filter(pk=user.pk).get()

        available_lectors = DefineModelsMixin.get_lectors_by_training(self.object, list_csv=True)

        context['booking_user_profile'] = booking_user_profile
        context['user'] = user
        context['available_lectors'] = available_lectors

        return context


class TrainingUpdateView(LoginRequiredMixin, IsStaffdMixin, views.UpdateView):
    model = Training
    template_name = 'trainings/edit-training.html'
    fields = '__all__'

    def get_success_url(self):
        return reverse_lazy('details training', kwargs={'slug': self.object.slug})


class TrainingDeleteView(LoginRequiredMixin, IsStaffdMixin, views.DeleteView):
    model = Training
    template_name = 'trainings/delete-training.html'
    success_url = reverse_lazy('trainings')

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        for field_name in form.fields:
            # form.fields[field_name].widget.attrs['readonly'] = True
            form.fields[field_name].widget.attrs['disabled'] = True
        return form
