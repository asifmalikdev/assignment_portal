from django.urls import path

from .views import AssignmentDashboardView, SubmissionCreateView

urlpatterns = [
    path('assignment_dashboard/', AssignmentDashboardView.as_view(), name='assignment_dashboard'),
    path("submit_assign/", SubmissionCreateView.as_view(), name="submit_assign"),
]