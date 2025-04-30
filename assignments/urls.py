from django.urls import path, include
from .views import (AssignmentDashboardView, AssignmentDeleteView,
                    SubmissionDashboardView, AssignmentViewSet,
                    AssignmentSubmissionViewSet, AssignmentQuestionViewSet)
from rest_framework.routers import DefaultRouter
#
# router = DefaultRouter()
# router.register(r'assignments', AssignmentViewSet)
# router.register(r'questions', AssignmentQuestionViewSet)
# router.register(r'submission', AssignmentSubmissionViewSet)
# urlpatterns = [
#     path('assignment_dashboard/', AssignmentDashboardView.as_view(), name='assignment_dashboard'),
#     path('assignment/<int:pk>/', AssignmentDashboardView.as_view(), name='assignment_edit'),
#     path('assignment/<int:pk>/delete/', AssignmentDeleteView.as_view(), name='assignment_delete'),
#     path("submission_dashboard/", SubmissionDashboardView.as_view(), name="submission_dashboard"),
#     path('api/', include(router.urls))
# ]