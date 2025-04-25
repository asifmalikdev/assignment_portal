from django import forms
from django.core.exceptions import ValidationError
from .models import Assignment, Submission
from django.utils import timezone


class AssignmentForm(forms.ModelForm):
    due_date = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'}),
        label="Due Date"
    )
    class Meta:
        model = Assignment
        fields = '__all__'

    def clean(self):
        cleaned_data = super().clean()
        teacher = cleaned_data.get('assigned_by')
        class_ = cleaned_data.get('assigned_to')
        if not teacher:
            raise ValidationError("Select the teacher who is assigning")
        if not class_:
            raise ValidationError("Select the class please")
        if teacher and class_ and not teacher.assigned_classes.filter(id = class_.id).exists():
            raise ValidationError("Teacher Can only assign to their own classes")

        return cleaned_data


class SubmissionForm(forms.ModelForm):
    class Meta:
        model = Submission
        fields = ['assignment', 'submitted_by', 'file', 'comment']  # 'submitted_by' is correct

    def clean_file(self):
        file = self.cleaned_data.get('file')
        if not file:
            raise ValidationError("Please upload a file.")

        if file.size > 10 * 1024 * 1024:  # 10MB limit
            raise ValidationError("File size must be under 10MB.")

        allowed_types = ['application/pdf', 'application/msword',
                         'application/vnd.openxmlformats-officedocument.wordprocessingml.document']
        if file.content_type not in allowed_types:
            raise ValidationError("Only PDF or Word documents are allowed.")

        return file

    def clean(self):
        cleaned_data = super().clean()
        assignment = cleaned_data.get('assignment')
        submitted_by = cleaned_data.get('submitted_by')

        if assignment and submitted_by:
            # ✅ Check if assignment is still open
            if assignment.due_date < timezone.now().date():
                raise ValidationError("The due date for this assignment has passed.")

            # ✅ Ensure student belongs to the class assigned the assignment
            if submitted_by.student_class != assignment.assigned_to:
                raise ValidationError("This student is not in the class assigned to this assignment.")

        return cleaned_data