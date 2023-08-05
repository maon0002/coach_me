from django.urls import path, include
from coach_me.lectors.views import LectorListView, LectorDetailsView, LectorUpdateView, LectorDeleteView, \
    LectorCreateView

urlpatterns = (
    path('lectors/', LectorListView.as_view(), name='lectors'),
    path('lectors/add/', LectorCreateView.as_view(), name='add lector'),

    path('lector/<slug:slug>/', include([
        path('details/', LectorDetailsView.as_view(), name='details lector'),
        path('edit/', LectorUpdateView.as_view(), name='edit lector'),
        path('delete/', LectorDeleteView.as_view(), name='delete lector'),
    ])),

)
