# urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('protected/', views.protected_view, name='protected'),
    path('signup/', views.signup, name='signup'),
    path('login/', views.login, name='login'),
    path('teacher-dashboard/', views.teacher_only_view),
    path('student-dashboard/', views.student_only_view),
    path('dashboard/', views.dashboard_view, name='dashboard'),

]
