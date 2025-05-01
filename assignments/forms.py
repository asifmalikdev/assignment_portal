from django import forms
from django.core.exceptions import ValidationError
from rest_framework.validators import qs_exists

from .models import Assignment, AssignmentQuestion, AssignmentQuestionThrough


class AssignmentAdminForm(forms.ModelForm):
    class Meta:
        model = Assignment
        fields = '__all__'

    def clean(self):
        cleaned_data = super().clean()
        assigned_by = cleaned_data.get('assigned_by')
        questions = cleaned_data.get('questions')
        assigned_to = cleaned_data.get('assigned_to')

        if assigned_by and questions:
            invalid_questions = questions.exclude(teacher=assigned_by)
            if invalid_questions.exists():
                raise ValidationError("questions do not belong to the selected teacher.")
        if assigned_to and questions:
            invalid=questions.exclude(assigned_class = assigned_to)
            if invalid.exists():
                raise ValidationError("some question are not for this class")
        return cleaned_data


class AssignmentQuestionInlineForm(forms.ModelForm):
    class Meta:
        model = AssignmentQuestion
        fields = '__all__'

    def clean(self):
        cleaned_data = super().clean()
        if cleaned_data.get('question_type') == 'MCQ':
            required = ['option_a', 'option_b', 'option_c', 'option_d', 'correct_option']
            for field in required:
                if not cleaned_data.get(field):
                    raise ValidationError("All options and correct answer are required for MCQs.")
        return cleaned_data
