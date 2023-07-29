from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.forms import modelform_factory
from django.urls import reverse_lazy
from django.views import generic as views
from coach_me.lectors.models import Lector
from coach_me.bookings.mixins import DisabledFormFieldsMixin
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page

UserModel = get_user_model()


class LectorListView(views.ListView):
    model = Lector
    template_name = 'lectors/lectors.html'

    # @method_decorator(cache_page(1))  # Cache will expire in 1 hour (3600 seconds)
    # def dispatch(self, *args, **kwargs):
    #     return super().dispatch(*args, **kwargs)


class LectorCreateView(LoginRequiredMixin, views.CreateView):
    model = Lector
    template_name = 'lectors/create-lector.html'
    fields = '__all__'
    success_url = reverse_lazy('add training')


class LectorDetailsView(views.DetailView):
    model = Lector
    template_name = 'lectors/details-lector.html'


class LectorUpdateView(LoginRequiredMixin, views.UpdateView):
    model = Lector
    template_name = 'lectors/edit-lector.html'
    fields = '__all__'

    def get_success_url(self):
        return reverse_lazy('details training', kwargs={'pk': self.object.pk})


class LectorDeleteView(LoginRequiredMixin, DisabledFormFieldsMixin, views.DeleteView):
    model = Lector
    template_name = 'lectors/delete-lector.html'
    form_class = modelform_factory(
        Lector,
        fields='__all__'
    )

    def get_form_kwargs(self):
        instance = self.get_object()
        form_kwargs = super().get_form_kwargs()

        form_kwargs.update(instance=instance)
        return form_kwargs
