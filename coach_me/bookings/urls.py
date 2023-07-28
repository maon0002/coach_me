from django.urls import path, include
from coach_me.bookings.views import IndexView, \
    BookingUpdateView, BookingDeleteView, BookingDetailsView, BookingCreateView


urlpatterns = (
    path('', IndexView.as_view(), name='index'),
    path('booking/add/', BookingCreateView.as_view(), name='add booking'),
    path('booking/<int:pk>/', include([
        path('details/', BookingDetailsView.as_view(), name='details booking'),
        path('edit/', BookingUpdateView.as_view(), name='edit booking'),
        path('delete/', BookingDeleteView.as_view(), name='delete booking'),
    ])),
)
