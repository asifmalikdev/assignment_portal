from rest_framework.exceptions import ValidationError
from django import forms
from .models import Role, District, School, Class, Student,Teacher

class RoleForm(forms.ModelForm):
    class Meta:
        model = Role
        fields = ['name', 'is_active']
    def clean(self):
        cleaned_data = super().clean()
        role_name = cleaned_data.get('name')

class DistrictForm(forms.ModelForm):
    class Meta:
        model = District
        fields = ['name', 'is_active']

class SchoolForm(forms.ModelForm):
    class Meta:
        model = School
        fields = ['name', 'address','district', 'principal', 'is_active']

class ClassForm(forms.ModelForm):
    class Meta:
        model = Class
        fields = ['name', 'grade_level', 'school', 'is_active']

class DistrictFilterForm(forms.Form):
    district = forms.ModelChoiceField(
        queryset=District.objects.all(),
        label="Select District",
        empty_label="Chose a district"

    )
    is_active_only = forms.BooleanField(
        required=False,
        initial=True,
        label="Only show active schools"
    )






class TeacherForm(forms.ModelForm):
    class Meta:
        model = Teacher
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Default empty queryset
        self.fields['assigned_classes'].queryset = Class.objects.none()

        # If 'school' is in form data, filter the assigned_classes based on the selected school
        if 'school' in self.data:
            try:
                school_id = int(self.data.get('school'))
                self.fields['assigned_classes'].queryset = Class.objects.filter(school_id=school_id)
            except (ValueError, TypeError):
                pass
        elif self.instance.pk and self.instance.school:
            self.fields['assigned_classes'].queryset = self.instance.school.School_Classes.all()


class AddStudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ['id', 'name', 'email', 'address', 'school', 'student_class', 'is_active']

        def clean(self):
            cleaned_data = super().clean()
            school = cleaned_data.get('school')
            student_class = cleaned_data.get('class')

            if student_class and school:
                if student_class.school != school:
                    raise ValidationError("Selected Class does not belong to the selected school")

            return cleaned_data




