from django.contrib import admin
from .models import Assignment, AssignmentSubmission, AssignmentMark

@admin.register(Assignment)
class AssignmentAdmin(admin.ModelAdmin):
    list_display = ('title', 'teacher', 'subject', 'classroom', 'due_time', 'created_at')
    list_filter = ('subject', 'teacher', 'classroom')
    search_fields = ('title', 'description')


@admin.register(AssignmentSubmission)
class AssignmentSubmissionAdmin(admin.ModelAdmin):
    list_display = ('assignment', 'student', 'submitted_at', 'status')
    list_filter = ('status', 'submitted_at')
    search_fields = ('assignment__title', 'student__user__username')


@admin.register(AssignmentMark)
class AssignmentMarkAdmin(admin.ModelAdmin):
    list_display = ('submission', 'marks', 'marked_by', 'marked_at')
    list_filter = ('marked_by', 'marked_at')
    search_fields = ('submission__assignment__title', 'submission__student__user__username')
