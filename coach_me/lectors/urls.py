from django.urls import path, include
from coach_me.lectors.views import LectorListView, LectorDetailsView, LectorUpdateView, LectorDeleteView

urlpatterns = (
    path('lectors/', LectorListView.as_view(), name='lectors'),

    path('lector/<int:pk>/', include([
        path('details/', LectorDetailsView.as_view(), name='details training'),
        path('edit/', LectorUpdateView.as_view(), name='edit training'),
        path('delete/', LectorDeleteView.as_view(), name='delete training'),
    ])),

)
