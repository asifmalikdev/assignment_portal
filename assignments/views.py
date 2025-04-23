
from .serializers import (AssignmentSerializer, AssignmentMarkSerializer, AssignmentSubmissionSerializer)
from .models import Assignment, AssignmentMark, AssignmentSubmission
from rest_framework import generics, permissions
from rest_framework.exceptions import PermissionDenied
from users.models import TeacherProfile, StudentProfile
class AssignmentCreateView(generics.CreateAPIView):
    queryset = Assignment.objects.all()
    serializer_class = AssignmentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        user = self.request.user
        if not hasattr(user, 'teacherprofile'):
            raise PermissionDenied("only teacher can create assignments")
        serializer.save(teacher = user.teacherprofile)

class AssignmentListView(generics.ListAPIView):
    serializer_class = AssignmentSerializer
    permission_classes = [permissions.IsAuthenticated]
    def get_queryset(self):
        user = self.request.user
        if not hasattr(user, 'studentprofile'):
            raise PermissionDenied("only student van view this")
        student = user.studentprofile
        return Assignment.objects.filter(classroom = student.classroom)
class AssignmentSubmissionView(generics.CreateAPIView):
    queryset = AssignmentSubmission.objects.all()
    serializer_class = AssignmentSubmissionSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        user = self.request.user
        if not hasattr(user, 'studentprofile'):
            raise PermissionDenied("Only students can submit assignments.")
        serializer.save(student=user.studentprofile)


class AssignmentMarkView(generics.CreateAPIView):
    queryset = AssignmentMark.objects.all()
    serializer_class = AssignmentMarkSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        user = self.request.user
        if not hasattr(user, 'teacherprofile'):
            raise PermissionDenied("Only teachers can mark assignments.")
        serializer.save(marked_by=user.teacherprofile)

