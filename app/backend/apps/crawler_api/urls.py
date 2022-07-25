from django.urls import path

from .views import Status, Tasks


urlpatterns = [
    path('tasks', Tasks.as_view()),
    path('tasks/status', Status.as_view()),
]
