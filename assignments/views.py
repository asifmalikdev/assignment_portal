from django.urls import reverse
from django.views.generic import TemplateView
from django.shortcuts import render, redirect, get_object_or_404
from .models import Assignment, AssignmentQuestion, AssignmentAttempt, Answer, AssignmentSubmission
from .forms import AssignmentAdminForm, AssignmentQuestionInlineForm, AssignmentSubmissionForm
from django.utils import timezone
from django.views import View
from django.http import Http404
from role.models import Class, Student


class AssignmentDashboardView(TemplateView):
    template_name = 'assignment_dashboard.html'

    def get(self, request):
        form = AssignmentAdminForm()
        assignments = Assignment.objects.all()
        return render(request, self.template_name, {'form': form, 'assignments': assignments})

    def post(self, request):
        if 'add' in request.POST:
            form = AssignmentAdminForm(request.POST)
            if form.is_valid():
                form.save()
                return redirect('assignment_dashboard')
        elif 'edit_id' in request.POST:
            obj = get_object_or_404(Assignment, pk=request.POST['edit_id'])
            form = AssignmentAdminForm(request.POST, instance=obj)
            if form.is_valid():
                form.save()
                return redirect('assignment_dashboard')
        elif 'delete_id' in request.POST:
            obj = get_object_or_404(Assignment, pk=request.POST['delete_id'])
            obj.delete()
            return redirect('assignment_dashboard')

        # fallback
        assignments = Assignment.objects.all()
        return render(request, self.template_name, {'form': form, 'assignments': assignments})




class AssignmentQuestionDashboardView(View):
    template_name = 'question_dashboard.html'
    def get(self, request):
        questions = AssignmentQuestion.objects.all()
        form = AssignmentQuestionInlineForm()
        return render(request, self.template_name, {
            'questions': questions,
            'form': form
        })

    def post(self, request):
        if 'create' in request.POST:
            form = AssignmentQuestionInlineForm(request.POST)
            if form.is_valid():
                form.save()
                return redirect('submission_dashboard')
        elif 'edit' in request.POST:
            question_id = request.POST.get('edit')
            try:
                question = AssignmentQuestion.objects.get(id=question_id)
            except AssignmentQuestion.DoesNotExist:
                raise Http404("Question not found")
            form = AssignmentQuestionInlineForm(request.POST, instance=question)
            if form.is_valid():
                form.save()
                return redirect('submission_dashboard')
        elif 'delete' in request.POST:
            question_id = request.POST.get('delete')
            try:
                question = AssignmentQuestion.objects.get(id=question_id)
                question.delete()
            except AssignmentQuestion.DoesNotExist:
                raise Http404("Question not found")
            return redirect('submission_dashboard')

        return redirect('submission_dashboard')


class FilteredAssignmentView(View):
    template_name = 'filtered_assignments.html'

    def get(self, request):
        classes = Class.objects.all()
        students = Student.objects.none()
        assignments = []

        selected_class = request.GET.get('class_id')
        selected_student = request.GET.get('student_id')

        if selected_class:
            students = Student.objects.filter(student_class__id=selected_class)
            if selected_student:
                # All assignments for the class
                class_assignments = Assignment.objects.filter(assigned_to__id=selected_class)

                # Assignments already submitted by the student
                submitted_assignments = AssignmentSubmission.objects.filter(
                    assignment__in=class_assignments,
                    student__id=selected_student
                ).values_list('assignment_id', flat=True)

                # Filter assignments that are NOT submitted
                assignments = Assignment.objects.filter(
                    assigned_to_id = selected_class
                ).exclude(
                    id__in=AssignmentSubmission.objects.filter(student_id=selected_student).values_list('assignment_id',
                                                                                                        flat=True)
                ).prefetch_related('questions')

        context = {
            'classes': classes,
            'students': students,
            'assignments': assignments,
            'selected_class': selected_class,
            'selected_student': selected_student,
        }
        return render(request, self.template_name, context)


from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

class SubmitAssignmentView(View):
    def post(self, request, assignment_id):
        assignment = get_object_or_404(Assignment, pk=assignment_id)
        student_id = request.POST.get('student_id')
        submitted_file = request.FILES.get('submitted_file')

        if not student_id or not submitted_file:
            return render(request, 'error.html', {'message': 'Missing student or file.'})

        student = get_object_or_404(Student, pk=student_id)

        AssignmentSubmission.objects.create(
            assignment=assignment,
            student=student.user,  # Assuming `Student` has OneToOneField to `User`
            submitted_file=submitted_file
        )

        return redirect('some-success-page')  # Replace with appropriate redirect

