# from django.urls import path, include
# # from coach_me.bookings.views import DashboardView
# from coach_me.profiles.views import ProfileDetailsView, ProfileUpdateView, \
#     ProfileDeleteView, DashboardView, CompanyCreateView, CompanyListView, CompanyDetailsView, CompanyUpdateView, \
#     CompanyDeleteView
#
# urlpatterns = (
#     # path('profile/<int:pk>/dashboard/', DashboardView.as_view(), name='dashboard'),
#     path('profile/', include([
#         path('<int:pk>/details/', ProfileDetailsView.as_view(), name='details profile'),
#         path('<int:pk>/edit/', ProfileUpdateView.as_view(), name='edit profile'),
#         path('<int:pk>/delete/', ProfileDeleteView.as_view(), name='delete profile'),
#         path('<int:pk>/dashboard/', DashboardView.as_view(), name='dashboard'),
#     ])),
#
#     path('company/add/', CompanyCreateView.as_view(), name='add company'),
#     path('companies/', CompanyListView.as_view(), name='companies'),
#
#     path('company/', include([
#         path('<slug:slug>/details/', CompanyDetailsView.as_view(), name='details company'),
#         path('<slug:slug>/edit/', CompanyUpdateView.as_view(), name='edit company'),
#         path('<slug:slug>/delete/', CompanyDeleteView.as_view(), name='delete company'),
#
#     ])),
#
# )
from . import views
from django.urls import path, include
from coach_me.profiles.views import ProfileDetailsView, ProfileUpdateView, ProfileDeleteView, DashboardView, \
    CompanyCreateView, CompanyListView, CompanyDetailsView, CompanyUpdateView, CompanyDeleteView

urlpatterns = [
    path('profile/', include([
        path('<int:pk>/details/', ProfileDetailsView.as_view(), name='details profile'),
        path('<int:pk>/edit/', ProfileUpdateView.as_view(), name='edit profile'),
        path('<int:pk>/delete/', ProfileDeleteView.as_view(), name='delete profile'),
        path('<int:pk>/dashboard/', DashboardView.as_view(), name='dashboard'),
    ])),

    path('company/add/', CompanyCreateView.as_view(), name='add company'),
    path('companies/', CompanyListView.as_view(), name='companies'),

    path('company/', include([
        path('<slug:slug>/details/', CompanyDetailsView.as_view(), name='details company'),
        path('<slug:slug>/edit/', CompanyUpdateView.as_view(), name='edit company'),
        path('<slug:slug>/delete/', CompanyDeleteView.as_view(), name='delete company'),
    ])),
    # Add a URL pattern for CSV export
    path('export-csv/', views.export_csv, name='export_csv'),
]
