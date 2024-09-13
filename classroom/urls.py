from django.urls import path
from .views import ClassroomView

app_name = 'classroom'

urlpatterns = [
    path('alunos/agendar-aulas', ClassroomView.as_view(), name='classroom-list-create'),
    path('alunos/atualizar-aula/<int:pk>', ClassroomView.as_view(), name='teacher-classroom')
]