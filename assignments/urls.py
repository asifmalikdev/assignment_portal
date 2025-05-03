
from django.urls import path
from .views import AssignmentDashboardView, AssignmentQuestionDashboardView,  FilteredAssignmentView, SubmitAssignmentView

urlpatterns = [

    path('assignments/', AssignmentDashboardView.as_view(), name='assignment_dashboard'),
    path('questions/', AssignmentQuestionDashboardView.as_view(), name='submission_dashboard'),
    path('filter-assignments/', FilteredAssignmentView.as_view(), name = 'filter-assignments'),
    path('submit-assignment/<int:assignment_id>/', SubmitAssignmentView.as_view(), name='submit-assignment'),

]












# from django.urls import path, include
# from .views import (AssignmentDashboardView, AssignmentQuestionDashboardView,
#                     SubmissionDashboardView, AssignmentViewSet,
#                     AssignmentSubmissionViewSet, AssignmentQuestionViewSet, AddQuestionFromAssignmentView)
# from rest_framework.routers import DefaultRouter
# #
# # router = DefaultRouter()
# # router.register(r'assignments', AssignmentViewSet)
# router.register(r'questions', AssignmentQuestionViewSet)
# # router.register(r'submission', AssignmentSubmissionViewSet)
# # urlpatterns = [
# #     path('assignment_dashboard/', AssignmentDashboardView.as_view(), name='assignment_dashboard'),
# #     path('assignments/add-question/', AddQuestionFromAssignmentView.as_view(), name='add_question_from_assignment'),
# #     path('question_dashboard/', AssignmentQuestionDashboardView.as_view(), name='question_dashboard')
# #     path("submission_dashboard/", SubmissionDashboardView.as_view(), name="submission_dashboard"),
# #     path('api/', include(router.urls))
# # ]

