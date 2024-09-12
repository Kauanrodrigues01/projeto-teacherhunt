from django.urls import path
from .views import ClassroomCreateView

app_name = 'classroom'

urlpatterns = [
    path('classrooms', ClassroomCreateView.as_view(), name='classroom-list-create'), 
]