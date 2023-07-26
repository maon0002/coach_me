from django.shortcuts import render
from django.urls import path, include
from coach_me.bookings.views import IndexView, \
    BookingUpdateView, BookingDeleteView, BookingDetailsView, BookingCreateView, TrainingCreateView, \
    TrainingDetailsView, TrainingUpdateView, TrainingDeleteView, TrainingListView, LectorListView

urlpatterns = (
    path('', IndexView.as_view(), name='index'),

    path('trainings/', TrainingListView.as_view(), name='trainings'),
    path('lectors/', LectorListView.as_view(), name='lectors'),

    path('training/add/', TrainingCreateView.as_view(), name='add training'),

    path('training/<int:pk>/', include([
        path('details/', TrainingDetailsView.as_view(), name='details training'),
        path('edit/', TrainingUpdateView.as_view(), name='edit training'),
        path('delete/', TrainingDeleteView.as_view(), name='delete training'),
    ])),

    path('booking/add/', BookingCreateView.as_view(), name='add booking'),

    path('booking/<int:pk>/', include([
        # path('add/', BookingCreateView.as_view(), name='add booking'),
        path('details/', BookingDetailsView.as_view(), name='details booking'),
        path('edit/', BookingUpdateView.as_view(), name='edit booking'),
        path('delete/', BookingDeleteView.as_view(), name='delete booking'),
    ])),

)
