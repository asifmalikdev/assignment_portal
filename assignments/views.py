from django.shortcuts import render
from django.views.generic.edit import CreateView
from rest_framework.reverse import reverse_lazy

from .models import Assignment, Submission
from .forms import AssignmentForm, SubmissionForm


class AssignmentCreateView(CreateView):
    model = Assignment
    form_class = AssignmentForm
    template_name = "assignment_form.html"
    success_url = reverse_lazy('add_assignment')

class SubmissionCreateView(CreateView):
    model = Submission
    form_class = SubmissionForm
    template_name = 'submission_form.html'
    success_url = reverse_lazy('submit_assign')