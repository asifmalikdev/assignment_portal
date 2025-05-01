from django.urls import reverse
from django.views.generic import TemplateView
from django.shortcuts import render, redirect, get_object_or_404
from .models import Assignment, AssignmentQuestion
from .forms import AssignmentAdminForm, AssignmentQuestionInlineForm


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

from django.shortcuts import render, redirect
from django.views import View
from .models import AssignmentQuestion
from .forms import AssignmentQuestionInlineForm
from django.http import Http404

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
