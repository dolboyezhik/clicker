from django.urls import path
from . import views


urlpatterns = [
    path('note/', views.NoteView.as_view(), name='note'),
]