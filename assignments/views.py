from cloudinit.config.schema import ValidationError
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import TemplateView, CreateView
from rest_framework.reverse import reverse_lazy

from .models import Assignment, Submission, AssignmentQuestion
# from .forms import AssignmentForm, SubmissionForm, AssignmentQuestionFromSet
from django.views import View
from django.contrib import messages
from django.utils import timezone
from django.db import transaction

class AssignmentDashboardView(View):
    template_name = 'assignment_dashboard.html'
    def get(self, request, pk=None, delete=None):
        if delete:
            assignment = get_object_or_404(Assignment, pk=delete)
            assignment.delete()
            return redirect('assignment_dashboard')
        if pk:
            assignment = get_object_or_404(Assignment, pk=pk)
            form = AssignmentForm(instance=assignment)
            formset = AssignmentQuestionFromSet(instance = assignment)
        else:
            assignment = None
            form = AssignmentForm()
            formset = AssignmentQuestionFromSet()
        assignments = Assignment.objects.all().order_by('-created_at')
        return render(request, self.template_name, {
            'form': form,
            'formset': formset,
            "assignments": assignments,
            'editing': assignment

        })
    def post(self, request, pk =None):
        if pk:
            assignment = get_object_or_404(Assignment, pk=pk)
            form = AssignmentForm(request.POST, instance=assignment)
            formset = AssignmentQuestionFromSet(request.POST, instance = assignment)
        else:
            form = AssignmentForm(request.POST)
            formset = AssignmentQuestionFromSet(request.POST)
        if form.is_valid() and formset.is_valid():
            assignment=form.save()
            formset.instance = assignment
            formset.save()
            return redirect('assignment_dashboard')
        assignments = Assignment.objects.all().order_by('-created_at')
        return render(request, self.template_name, {
            'form': form,
            'formset': formset,
            'assignments': assignments,
            'editing': assignment if pk else None
        })
class AssignmentDeleteView(View):
    def get(self, request, pk):
        assignment = get_object_or_404(Assignment, pk=pk)
        assignment.delete()
        messages.success(request, "Assignment deleted successfully.")
        return redirect('assignment_dashboard')

# class AssignmentDashboardView(CreateView):
#     model = Assignment
#     form_class = AssignmentForm
#     template_name = 'assignment_dashboard.html'
#     success_url = reverse_lazy('assignment_dashboard')
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         if self.request.POST:
#             context['formset'] = AssignmentQuestionFromSet(self.request.POST)
#         else:
#             context['formset'] = AssignmentQuestionFromSet
#         return context
#     def form_valid(self, form):
#         context = self.get_context_data()
#         formset = context['formset']
#         if form.is_valid() and formset.is_valid():
#             try:
#                 with transaction.atomic():
#                     self.object = form.save()
#                     formset.instance = self.object
#                     formset.save()
#                     messages.success(self.request, 'assignment create scuccessfully')
#                     return redirect(self.success_url)
#             except Exception as e:
#                 messages.error(self.request,f'an error occurred: {e}')
#         else:
#             messages.error(self.request, 'pleae fix the error below')
#         return self.render_to_response(self.get_context_data(form=form))


# class AssignmentDashboardView(TemplateView):
#     template_name = 'assignment_form.html'
#     def get(self, request):
#         form = AssignmentForm()
#         search_query = request.GET.get('search', '')
#         class_filter = request.GET.get('class_filter')
#         teacher_filter = request.GET.get('teacher_filter')
#
#         assignments = Assignment.objects.all()
#
#         if search_query:
#             assignments = assignments.filter(
#                 Q(title__icontains=search_query) | Q(description__icontains=search_query)
#             )
#         if class_filter:
#             assignments = assignments.filter(assigned_to__id=class_filter)
#         if teacher_filter:
#             assignments = assignments.filter(assigned_by__id=teacher_filter)
#
#         classes = Class.objects.all()
#         teachers = Teacher.objects.all()
#         context = {
#             'form': form,
#             'assignments': assignments,
#             'classes': classes,
#             'teachers': teachers
#         }
#         return render(request, self.template_name, context)
#
#     def post(self, request):
#         if 'delete_btn' in request.POST:
#             assignment_id = request.POST.get('assignment_id')
#             assignment = get_object_or_404(Assignment, pk=assignment_id)
#             assignment.delete()
#             return redirect('assignment_dashboard')
#
#         assignment_id = request.POST.get('assignment_id')
#         instance = Assignment.objects.filter(pk=assignment_id).first() if assignment_id else None
#         form = AssignmentForm(request.POST, instance=instance)
#
#         if form.is_valid():
#             form.save()
#             return redirect('assignment_dashboard')
#
#         assignments = Assignment.objects.all()
#         classes = Class.objects.all()
#         teachers = Teacher.objects.all()
#         context = {
#             'form': form,
#             'assignments': assignments,
#             'classes': classes,
#             'teachers': teachers,
#         }
#         return render(request, self.template_name, context)


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

from .serializers import AssignmentSerializer, AssignmentQuestionSerializer, SubmissionSerializer
from rest_framework import viewsets
class AssignmentViewSet(viewsets.ModelViewSet):
    queryset = Assignment.objects.all()
    serializer_class = AssignmentSerializer

class AssignmentQuestionViewSet(viewsets.ModelViewSet):
    queryset = AssignmentQuestion.objects.all()
    serializer_class = AssignmentQuestionSerializer
class AssignmentSubmissionViewSet(viewsets.ModelViewSet):
    queryset = Submission.objects.all()
    serializer_class = SubmissionSerializer
