from django.urls import path

from .views import AssignmentDashboardView, SubmissionDashboardView

urlpatterns = [
    path('assignment_dashboard/', AssignmentDashboardView.as_view(), name='assignment_dashboard'),
    path("submission_dashboard/", SubmissionDashboardView.as_view(), name="submission_dashboard"),
]