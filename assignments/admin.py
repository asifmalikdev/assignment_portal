from django.contrib import admin
from .models import Assignment, Submission
@admin.register(Assignment)
class AssignmentAdmin(admin.ModelAdmin):
    list_display = ('id', 'title','assigned_by','assigned_to', 'due_date', 'created_at',)
    search_fields = ('title', 'description',)
    list_filter = ('assigned_to', 'assigned_by', 'due_date',)


@admin.register(Submission)
class SubmissionAdmin(admin.ModelAdmin):
    list_display = ('id', 'assignment', 'submitted_by', 'submitted_at')
    search_fields = ('assignment__title', 'submitted_by__name')
    list_filter = ('submitted_at', 'assignment')