from django.urls import path

from NOTE import views


urlpatterns = [
    path('notes/', views.NoteListCreateAPIView.as_view()),
    path('notes/<int:pk>', views.NoteDetailUpdateDeleteAPIView.as_view()),
    ]
