from django.urls import path
from .views import ClassroomCreateView

app_name = 'classroom'

urlpatterns = [
    path('alunos/agendar-aulas', ClassroomCreateView.as_view(), name='classroom-list-create'), 
]