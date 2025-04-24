from django.shortcuts import render, redirect
from .forms import RoleForm, ClassForm, SchoolForm, DistrictForm, TeacherForm, AddStudentForm
from .models import District,  Student

def add_role(request):
    if request.method == "POST":
        form = RoleForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('admin')
    else:
        form = RoleForm()
    return render(request, "forms.html", {"form": form})

from django.views.generic.edit import CreateView
from django.urls import reverse_lazy


class District_Create_View(CreateView):
    model = District
    form_class = DistrictForm
    template_name = "district_form.html"
    success_url = reverse_lazy('admin')

def add_school(request):
    if request.method=="POST":
        form = SchoolForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('admin')
    else:
        form = SchoolForm()

    return render(request, "add_school.html", {"form":form})

def add_class(request):
    if request.method == "POST":
        form = ClassForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('add_class')

    else:
        form = ClassForm()
    return render(request, 'add_class.html', {'form': form})


def add_teacher(request):
    if request.method == "POST":
        form = TeacherForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('teacher_list')
    else:
        form = TeacherForm()
    return render(request, 'add_teacher.html', {'form': form})

def add_student(request):
    if request.method =="POST":
        form = AddStudentForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('add_student')

    else:
        form = AddStudentForm()

    return render(request, 'add_student.html', {'form':form})







from django.views import View
from .models import School
from .forms import DistrictFilterForm
class DistrictBasedView(View):
    template_name = "district_school_list.html"
    def get(self, request):
        form = DistrictFilterForm(request.GET or None)
        schools = None
        if form.is_valid():
            selected_district = form.cleaned_data['district']
            is_active_only=form.cleaned_data.get('is_active_only')
            schools = School.objects.filter(district = selected_district)
            if is_active_only:
                schools = schools.filter(is_active=True)
        return render(request, self.template_name, {'form':form, 'schools':schools})

