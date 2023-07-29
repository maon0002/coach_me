from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.forms import modelform_factory
from django.urls import reverse_lazy, reverse
from django.views import generic as views
from django.views.decorators.cache import cache_page
from coach_me.bookings.models import Booking, Lector
from coach_me.trainings.models import Training
from coach_me.bookings.mixins import DisabledFormFieldsMixin
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page

UserModel = get_user_model()


class TrainingListView(views.ListView):
    model = Training
    template_name = 'bookings/../../templates/trainings/trainings.html'

    # @method_decorator(cache_page(3600))  # Cache will expire in 1 hour (3600 seconds)
    # def dispatch(self, *args, **kwargs):
    #     return super().dispatch(*args, **kwargs)


class TrainingCreateView(LoginRequiredMixin, views.CreateView):
    model = Booking
    template_name = 'trainings/create-training.html'
    fields = '__all__'
    success_url = reverse_lazy('add training')


class TrainingDetailsView(views.DetailView):
    model = Training
    template_name = 'trainings/details-training.html'


class TrainingUpdateView(LoginRequiredMixin, views.UpdateView):
    model = Training
    template_name = 'trainings/edit-training.html'
    fields = '__all__'

    def get_success_url(self):
        return reverse_lazy('details training', kwargs={'pk': self.object.pk})


class TrainingDeleteView(LoginRequiredMixin, DisabledFormFieldsMixin, views.DeleteView):
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
