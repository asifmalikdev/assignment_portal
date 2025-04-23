from django.urls import path
from . import views
from .views import District_Create_View, DistrictBasedView

urlpatterns = [
    path("add/", views.add_role, name="add"),
    path("add_district/", District_Create_View.as_view(), name="add_district"),
    path("add_school/", views.add_school, name = "add_school"),
    path("schools_by_district/", DistrictBasedView.as_view(), name = "schools_by_district")
]