from django.shortcuts import render, redirect, get_object_or_404
from .forms import RoleForm, ClassForm, SchoolForm, DistrictForm, TeacherForm, AddStudentForm
from .models import District, Student, Class, Teacher
from django.views.generic import TemplateView, ListView
from django.views import View
from django.db.models import Q
from django.views.generic.edit import CreateView
from django.urls import reverse_lazy



def add_role(request):
    if request.method == "POST":
        form = RoleForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('admin')
    else:
        form = RoleForm()
    return render(request, "forms.html", {"form": form})



class District_Create_View(CreateView):
    model = District
    form_class = DistrictForm
    template_name = "district_form.html"
    success_url = reverse_lazy('admin')


class SchoolDashboardView(TemplateView):
    template_name = "school_dashboard.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        query = self.request.GET.get("q", "")
        schools = School.objects.filter(name__icontains=query) if query else School.objects.all()

        # If editing, load the school instance
        edit_id = self.request.GET.get("edit")
        instance = get_object_or_404(School, id=edit_id) if edit_id else None

        context["form"] = SchoolForm(instance=instance)
        context["schools"] = schools
        context["editing"] = instance is not None
        context["edit_id"] = edit_id
        return context

    def post(self, request, *args, **kwargs):
        if "delete" in request.POST:
            school = get_object_or_404(School, id=request.POST.get("delete"))
            school.delete()
            return redirect("school_dashboard")

        edit_id = request.POST.get("edit_id")
        instance = get_object_or_404(School, id=edit_id) if edit_id else None

        form = SchoolForm(request.POST, instance=instance)
        if form.is_valid():
            form.save()
            return redirect("school_dashboard")

        context = self.get_context_data()
        context["form"] = form
        context["editing"] = instance is not None
        context["edit_id"] = edit_id
        return self.render_to_response(context)




class ClassDashboardView(TemplateView):
    template_name = 'class_dashboard.html'
    def get(self, request, *args, **kwargs):
        search_query = request.GET.get("search", "")
        school_filter = request.GET.get('school', "")
        classes = Class.objects.all()
        if search_query:
            classes = classes.filter(name__icontains = search_query)
        if school_filter:
            classes = classes.filter(school_id = school_filter)
        context={
            "form": ClassForm(),
            "classes": classes,
            "schools": School.objects.filter(is_active=True),
            "search_query": search_query,
            "school_filter": school_filter
        }
        return self.render_to_response(context)
    def post(self, request, *args, **kwargs):
        form = ClassForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('class_dashboard')
        else:
            context={
                "form": form,
                "classes": Class.objects.all(),
                "schools":School.objects.filter(is_active=True),
            }
        return self.render_to_response(context)
    def post_edit(self, request, class_id):
        class_instance = get_object_or_404(Class, pk = class_id)
        form = ClassForm((request), instance=class_instance)
        if form.is_valid():
            form.save()
        return redirect("class_dashboard")
    def post_delete(self, request, class_id):
        class_instance = get_object_or_404(Class, pk = class_id)
        class_instance.delete()
        return redirect("class_dashboard")



class TeacherDashboardView(View):
    template_name = "teacher_dashboard.html"
    def get(self, request):
        search = request.GET.get('search','')
        school = request.GET.get('school')
        assigned_class = request.GET.get('assigned_class')
        edit_id = request.GET.get('edit_id')

        teachers = Teacher.objects.select_related('school').prefetch_related('assigned_classes').all()
        if search:
            teachers = teachers.filter(Q(name__icontains = search)| Q(email__icontains=search))

        if school:
            teachers = teachers.filter(school_id = school)
        if assigned_class:
            teachers = teachers.filter(assigned_classes__id = assigned_class)
        instance = Teacher.objects.get(pk=edit_id) if edit_id else None
        form = TeacherForm(instance=instance)
        context ={
            "teachers":teachers.distinct(),
            "form":form,
            "edit_id":edit_id,
            'schools': School.objects.all(),
            'classes': Class.objects.all(),
        }

        return render(request, self.template_name, context)

    def post(self,request):
        if 'delete_id' in request.POST:
            teacher = get_object_or_404(Teacher, pk = request.POST['delete_id'])
            teacher.delete()
            return redirect('teacher_dashboard')
        teacher_id = request.POST.get('edit_id')
        instance = get_object_or_404(Teacher, pk=teacher_id) if teacher_id else None

        form = TeacherForm(request.POST, instance=instance)
        if form.is_valid():
            form.save()
            return redirect('teacher_dashboard')
        teachers = Teacher.objects.all().selected_ralated('school').prefetch_related('assigned_classes')
        context ={
            'teachers':teachers,
            "form": form,
            'edit_id': teacher_id,
            'schools': School.objects.all(),
            'Classes': Class.objects.all(),
        }
        return render(request, self.template_name, context)





class StudentDashboardView(TemplateView):
    template_name = 'student_dashboard.html'
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Filters
        search_query = self.request.GET.get('search', '')
        school_filter = self.request.GET.get('school', '')
        class_filter = self.request.GET.get('student_class', '')

        students = Student.objects.all()
        if search_query:
            students = students.filter(Q(name__icontains=search_query) | Q(email__icontains=search_query))
        if school_filter:
            students = students.filter(school_id=school_filter)
        if class_filter:
            students = students.filter(student_class_id=class_filter)

        # Handle pagination manually if needed (you can use Paginator here)

        context['students'] = students
        context['schools'] = School.objects.all()
        context['classes'] = Class.objects.all()
        context['form'] = AddStudentForm()
        return context

    def post(self, request, *args, **kwargs):
        if 'delete_id' in request.POST:
            student = get_object_or_404(Student, id=request.POST.get('delete_id'))
            student.delete()
            return redirect('student_dashboard')

        if 'edit_id' in request.POST:
            student = get_object_or_404(Student, id=request.POST.get('edit_id'))
            form = AddStudentForm(request.POST, instance=student)
        else:
            form = AddStudentForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect('student_dashboard')

        # If invalid, render context again with form errors
        context = self.get_context_data()
        context['form'] = form
        return self.render_to_response(context)





















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

