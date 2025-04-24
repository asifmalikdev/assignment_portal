from django import forms
from .models import Assignment, Submission

class AssignmentForm(forms.ModelForm):
    due_date = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'}),
        label="Due Date"
    )
    class Meta:
        model = Assignment
        fields = ['title', 'description', 'due_date', 'assigned_by', 'assigned_to' ]

class SubmissionForm(forms.ModelForm):
    class Meta:
        model = Submission
        fields = ['assignment', 'student', 'file']