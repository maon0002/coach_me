from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin, IsStaffdMixin
from django.forms import modelform_factory
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse_lazy
from django.views import generic as views

from coach_me.lectors.forms import LectorList
from coach_me.lectors.models import Lector
from coach_me.bookings.mixins import DefineModelsMixin
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page

from coach_me.profiles.models import BookingUserProfile

UserModel = get_user_model()


class LectorListView(views.ListView):
    model = Lector
    template_name = 'lectors/lectors.html'
    form_class = LectorList

    # @method_decorator(cache_page(1))  # Cache will expire in 1 hour (3600 seconds)
    # def dispatch(self, *args, **kwargs):
    #     return super().dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        user = self.request.user
        context = super().get_context_data(**kwargs)
        # booking_user_profile = BookingUserProfile.objects.filter(pk=user.pk).get()
        # available_trainings = DefineModelsMixin.get_trainings_by_lector(self.object, True)
        #
        # context['available_lectors'] = available_trainings
        try:
            profile = BookingUserProfile.objects.get(pk=user.pk)
        except BookingUserProfile.DoesNotExist:
            profile = None

            context['booking_user_profile'] = profile
        context['user'] = user

        return context


class LectorCreateView(LoginRequiredMixin, IsStaffdMixin, views.CreateView):
    model = Lector
    template_name = 'lectors/create-lector.html'
    fields = '__all__'
    success_url = reverse_lazy('lectors')

    def form_valid(self, form):
        # Check if the BookingUser is already linked to another Lector

        lector_bookinguser_duplicate = Lector.objects.filter(
            user_id=form.instance.user_id,
        ).exists()

        if lector_bookinguser_duplicate:
            form.add_error(None, "This user was already linked to another Lector.")
            return self.form_invalid(form)

        return super().form_valid(form)


class LectorDetailsView(views.DetailView):
    model = Lector
    template_name = 'lectors/details-lector.html'

    def get_context_data(self, **kwargs):
        user = self.request.user
        context = super().get_context_data(**kwargs)
        booking_user_profile = BookingUserProfile.objects.filter(pk=user.pk).get()
        available_trainings = DefineModelsMixin.get_trainings_by_lector(self.object, False)

        context['booking_user_profile'] = booking_user_profile
        context['user'] = user
        context['available_trainings'] = available_trainings

        return context


class LectorUpdateView(LoginRequiredMixin, IsStaffdMixin, views.UpdateView):
    model = Lector
    template_name = 'lectors/edit-lector.html'
    fields = '__all__'

    def get_success_url(self):
        return reverse_lazy('details lector', kwargs={'slug': self.object.slug})


class LectorDeleteView(LoginRequiredMixin, IsStaffdMixin, views.DeleteView):
    model = Lector
    template_name = 'lectors/delete-lector.html'
    success_url = reverse_lazy('lectors')
    #
    #
    # def get_form(self, form_class=None):
    #     form = super().get_form(form_class)
    #     for field_name in form.fields:
    #         form.fields[field_name].widget.attrs['disabled'] = True
    #         # form.fields[field_name].widget.attrs['readonly'] = True
    #     return form
