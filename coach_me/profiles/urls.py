from django.urls import path, include
# from coach_me.bookings.views import DashboardView
from coach_me.profiles.views import ProfileDetailsView, ProfileUpdateView, \
    ProfileDeleteView, DashboardView

urlpatterns = (
    # path('profile/<int:pk>/dashboard/', DashboardView.as_view(), name='dashboard'),
    path('profile/', include([
        path('<int:pk>/details/', ProfileDetailsView.as_view(), name='details profile'),
        path('<int:pk>/edit/', ProfileUpdateView.as_view(), name='edit profile'),
        path('<int:pk>/delete/', ProfileDeleteView.as_view(), name='delete profile'),
        path('<int:pk>/dashboard/', DashboardView.as_view(), name='dashboard'),
    ])),


)
