from django.urls import path
from .views import (
    ClassList, ClassUpdate, ClassDestroy,
    SubjectList, SubjectseUpdate, SubjectDestroy,
    StudentList, StudentUpdate, StudentDestroy,
    RegistrUserView, LoginUserView
)

urlpatterns = [
    path('classes/', ClassList.as_view()),
    path('classes/<int:pk>/', ClassUpdate.as_view()),
    path('classes/<int:pk>/delete/', ClassDestroy.as_view()),

    path('subjects/', SubjectList.as_view()),
    path('subjects/<int:pk>/', SubjectseUpdate.as_view()),
    path('subjects/<int:pk>/delete/', SubjectDestroy.as_view()),

    path('students/', StudentList.as_view()),
    path('students/<int:pk>/', StudentUpdate.as_view()),
    path('students/<int:pk>/delete/', StudentDestroy.as_view()),

    path('register/', RegistrUserView.as_view()),
    path('login/', LoginUserView.as_view()),
]