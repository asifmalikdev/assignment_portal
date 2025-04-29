from django.contrib import admin
from .models import Assignment, AssignmentQuestion, Submission


class AssignmentQuestionInline(admin.TabularInline):
    model = AssignmentQuestion
    extra = 1  # Show 1 empty row by default
    min_num = 1
    verbose_name = "Question"
    verbose_name_plural = "Questions"


@admin.register(Assignment)
class AssignmentAdmin(admin.ModelAdmin):
    list_display = ('title', 'assigned_to', 'assigned_by', 'due_date', 'created_at')
    list_filter = ('assigned_to', 'assigned_by', 'due_date')
    search_fields = ('title', 'description')
    inlines = [AssignmentQuestionInline]


@admin.register(Submission)
class SubmissionAdmin(admin.ModelAdmin):
    list_display = ('assignment', 'submitted_by', 'submitted_at')
    list_filter = ('assignment__assigned_to', 'assignment', 'submitted_at')
    search_fields = ('assignment__title', 'submitted_by__name')
