from rest_framework import serializers
from .models import Assignment, AssignmentSubmission, AssignmentMark
from users.models import TeacherProfile, StudentProfile

class AssignmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Assignment
        fields = '__all__'
        read_only_fields = ['teacher', 'created_at']


class AssignmentSubmissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = AssignmentSubmission
        fields = '__all__'
        read_only_fields = ['student', 'submitted_at', 'status']
        def create(self, validated_data):
            assignment = validated_data['assignment']
            student = validated_data['student']
            submitted_at = validated_data.get('submitted_at')
            due_time = assignment.due_time
            current_time = submitted_at.time() if submitted_at else None
            status = 'submitted'
            if current_time and current_time>due_time:
                status = 'late'
            validated_data['status']=status
            return super().create(validated_data)

class AssignmentMarkSerializer(serializers.ModelSerializer):
    class Meta:
        model = AssignmentMark
        fields = '__all__'
        read_only_fields = ['marked_by', 'marked_at']