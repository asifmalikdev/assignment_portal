from django.urls import path
from . import views
from .views import District_Create_View, DistrictBasedView, AddStudentView

urlpatterns = [
    path("add/", views.add_role, name="add"),
    path("add_district/", District_Create_View.as_view(), name="add_district"),
    path("add_school/", views.add_school, name = "add_school"),
    path("schools_by_district/", DistrictBasedView.as_view(), name = "schools_by_district"),
    path("add_class/", views.add_class, name= "add_class"),
    path('teacher_list/', views.add_teacher, name="teacher_list"),
    path('add_student/', AddStudentView.as_view(), name="add_student"),

]