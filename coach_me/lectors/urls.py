from django.urls import path, include
from coach_me.lectors.views import LectorListView, LectorDetailsView, LectorUpdateView, LectorDeleteView

urlpatterns = (
    path('lectors/', LectorListView.as_view(), name='lectors'),

    path('lector/<int:pk>/', include([
        path('details/', LectorDetailsView.as_view(), name='details lector'),
        path('edit/', LectorUpdateView.as_view(), name='edit lector'),
        path('delete/', LectorDeleteView.as_view(), name='delete lector'),
    ])),

)
