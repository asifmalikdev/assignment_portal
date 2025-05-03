from cProfile import label

from django import forms
from django.core.exceptions import ValidationError
from pkg_resources import require

from .models import Assignment, AssignmentQuestion, AssignmentQuestionThrough, Answer


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

# assignment/forms.py
from django import forms
from .models import AssignmentQuestion, Assignment, Answer

class AssignmentSubmissionForm(forms.Form):
    def __init__(self, assignment, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for question in assignment.questions.all():
            field_name = f"question_{question.id}"
            if question.question_type == 'MCQ':
                choices = [
                    ('a', f"A. {question.option_a}"),
                    ('b', f"B. {question.option_b}"),
                    ('c', f"C. {question.option_c}"),
                    ('d', f"D. {question.option_d}")
                ]
                self.fields[field_name] = forms.ChoiceField(
                    label=question.text,
                    choices=choices,
                    widget=forms.RadioSelect,
                    required=False
                )
            else:
                self.fields[field_name] = forms.CharField(
                    label=question.text,
                    widget=forms.Textarea,
                    required=False
                )



