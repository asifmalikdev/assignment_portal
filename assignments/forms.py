from django.core.exceptions import ValidationError
from django.forms.models import inlineformset_factory
from django.utils import timezone
from django import forms
from .models import Assignment, AssignmentQuestion

class AssignmentForm(forms.ModelForm):
    class Meta:
        model = Assignment
        fields = '__all__'
    def clean_question(self):
        questions = self.cleaned_data.get('questions')
        teacher = self.cleaned_data.get('assigned_by')
        if teacher:
            invalid=questions.exclude(teacher=teacher)
            if invalid.exists():
                raise forms.ValidationError("One or Many Question selected are don't belong to this teacher")
            return questions



# AssignmentQuestionFromSet= inlineformset_factory(
#     Assignment,
#     AssignmentQuestion,
#     fields=['question_text','question_type', 'marks', 'option_a', 'option_b', 'option_c', 'option_d', 'correct_option'],
#     extra=1,
#     can_delete=True
# )
#
# class SubmissionForm(forms.ModelForm):
#     class Meta:
#         model = Submission
#         fields = ['assignment', 'submitted_by', 'file', 'comment']  # 'submitted_by' is correct
#
#     def clean_file(self):
#         file = self.cleaned_data.get('file')
#         if not file:
#             raise ValidationError("Please upload a file.")
#
#         if file.size > 10 * 1024 * 1024:  # 10MB limit
#             raise ValidationError("File size must be under 10MB.")
#
#         allowed_types = ['application/pdf', 'application/msword',
#                          'application/vnd.openxmlformats-officedocument.wordprocessingml.document']
#         if file.content_type not in allowed_types:
#             raise ValidationError("Only PDF or Word documents are allowed.")
#
#         return file
#
#     def clean(self):
#         cleaned_data = super().clean()
#         assignment = cleaned_data.get('assignment')
#         submitted_by = cleaned_data.get('submitted_by')
#
#         if assignment and submitted_by:
#             #date validation
#             if assignment.due_date < timezone.now().date():
#                 raise ValidationError("The due date for this assignment has passed.")
#
#             #student check on class
#             if submitted_by.student_class != assignment.assigned_to:
#                 raise ValidationError("This student is not in the class assigned to this assignment.")
#
#         return cleaned_data