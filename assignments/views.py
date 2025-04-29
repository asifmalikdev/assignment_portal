from cloudinit.config.schema import ValidationError
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import TemplateView
from django.views.generic.edit import CreateView
from rest_framework.reverse import reverse_lazy
from django.db.models import Q
from role.models import Class, Teacher
from .models import Assignment, Submission
from .forms import AssignmentForm, SubmissionForm
from django.views import View
from django.contrib import messages
from django.utils import timezone


class AssignmentDashboardView(TemplateView):
    template_name = 'assignment_form.html'
    def get(self, request):
        form = AssignmentForm()
        search_query = request.GET.get('search', '')
        class_filter = request.GET.get('class_filter')
        teacher_filter = request.GET.get('teacher_filter')

        assignments = Assignment.objects.all()

        if search_query:
            assignments = assignments.filter(
                Q(title__icontains=search_query) | Q(description__icontains=search_query)
            )
        if class_filter:
            assignments = assignments.filter(assigned_to__id=class_filter)
        if teacher_filter:
            assignments = assignments.filter(assigned_by__id=teacher_filter)

        classes = Class.objects.all()
        teachers = Teacher.objects.all()
        context = {
            'form': form,
            'assignments': assignments,
            'classes': classes,
            'teachers': teachers
        }
        return render(request, self.template_name, context)

    def post(self, request):
        if 'delete_btn' in request.POST:
            assignment_id = request.POST.get('assignment_id')
            assignment = get_object_or_404(Assignment, pk=assignment_id)
            assignment.delete()
            return redirect('assignment_dashboard')

        assignment_id = request.POST.get('assignment_id')
        instance = Assignment.objects.filter(pk=assignment_id).first() if assignment_id else None
        form = AssignmentForm(request.POST, instance=instance)

        if form.is_valid():
            form.save()
            return redirect('assignment_dashboard')

        assignments = Assignment.objects.all()
        classes = Class.objects.all()
        teachers = Teacher.objects.all()
        context = {
            'form': form,
            'assignments': assignments,
            'classes': classes,
            'teachers': teachers,
        }
        return render(request, self.template_name, context)


class SubmissionDashboardView(View):
    template_name = 'submission_dashboard.html'
    def get(self, request):
        form = SubmissionForm()
        submissions = Submission.objects.select_related('assignment', 'submitted_by').all()


        # we will use it later filter only current student's submissions
        # submissions = submissions.filter(submitted_by=request.user.student)
        context ={
            'form': form,
            'submissions':submissions
        }
        return  render(request, self.template_name, )

    def post(self, request):
        if 'delete_id' in request.POST:
            submission_id = request.POST.get('delete_id')
            submission = get_object_or_404(Submission, id = submission_id)
            submission.delete()
            messages.success(request, "submission deleted successfully")
            return redirect('submission_dashboard')
        form = SubmissionForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                form.save()
                messages.success(request, 'submission was successfully')
                return redirect('submission_dashboard')
            except ValidationError as e:
                form.add_error(None, e)
        else:
            messages.error(request, 'Please correct the error below')


        submissions = Submission.objects.select_related('assignment', 'submitted_by').all()
        context = {
            'form':form,
            'submissions': submissions
        }
        return render(request, self.template_name, context)

