from django.urls import path, include
from coach_me.trainings.views import TrainingCreateView, \
    TrainingDetailsView, TrainingUpdateView, TrainingDeleteView, TrainingListView

urlpatterns = (
    path('trainings/', TrainingListView.as_view(), name='trainings'),
    path('training/add/', TrainingCreateView.as_view(), name='add training'),

    path('training/<slug:slug>/', include([
        path('details/', TrainingDetailsView.as_view(), name='details training'),
        path('edit/', TrainingUpdateView.as_view(), name='edit training'),
        path('delete/', TrainingDeleteView.as_view(), name='delete training'),
    ])),

)