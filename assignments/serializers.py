from rest_framework import serializers
from .models import Assignment, AssignmentQuestion, Submission

class AssignmentQuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = AssignmentQuestion
        fields = '__all__'

class AssignmentSerializer(serializers.ModelSerializer):
    class Meta:
        model= Assignment
        fields = '__all__'



class SubmissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Submission
        fields= ['id', 'assignment', 'submitted_by', 'submitted_file', 'submitted_at', 'status']
