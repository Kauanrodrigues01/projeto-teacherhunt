from django.urls import path

from .views import DocsView


app_name = "core"
urlpatterns = [
    path("docs", DocsView.as_view(), name="docs"),
]
