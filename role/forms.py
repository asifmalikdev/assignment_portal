from django import forms
from .models import Role, District, School

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
        fields = ['name', 'address','district', 'is_active']

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



