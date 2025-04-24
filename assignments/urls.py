from django.urls import path

from .views import AssignmentCreateView, SubmissionCreateView

urlpatterns = [
    path("add_assignment/", AssignmentCreateView.as_view(), name="add_assignment"),
    path("submit_assign/", SubmissionCreateView.as_view(), name="submit_assign"),
]