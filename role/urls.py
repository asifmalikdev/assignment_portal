
from django.db import router
from django.urls import path, include
from . import views
from .admin import StudentAdmin
from .forms import AddStudentForm

from .views import (District_Create_View, DistrictBasedView,
                    SchoolDashboardView, ClassDashboardView,
                    TeacherDashboardView, StudentDashboardView, StudentViewSet)
from rest_framework.routers import DefaultRouter
router = DefaultRouter()
router.register(r'students', StudentViewSet, basename='student' )


urlpatterns = [
    path("add/", views.add_role, name="add"),
    path("add_district/", District_Create_View.as_view(), name="add_district"),
    path("schools/", SchoolDashboardView.as_view() , name = "school_dashboard"),
    path("schools_by_district/", DistrictBasedView.as_view(), name = "schools_by_district"),
    path("class_dashboard/", ClassDashboardView.as_view(), name= "class_dashboard"),
    path("class/delete/<int:class_id>/", ClassDashboardView.as_view(), name="delete_class"),
    path("class/edit/<int:class_id>/", ClassDashboardView.as_view(), name="edit_class"),
    path('teacher_dashboard/', TeacherDashboardView.as_view() , name="teacher_dashboard"),
    path('student_dashboard/', StudentDashboardView.as_view(), name="student_dashboard"),
    path('api/', include(router.urls))

]