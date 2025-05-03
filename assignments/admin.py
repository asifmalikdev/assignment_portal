from django.contrib import admin
from django.core.exceptions import ValidationError
from django import forms
from django.db import transaction

from .models import Assignment, AssignmentQuestion, AssignmentAttempt, Answer, AssignmentQuestionThrough
from .forms import AssignmentAdminForm, AssignmentQuestionInlineForm
from django.utils.html import format_html


# Inline for AssignmentQuestionThrough (linking model)
class AssignmentQuestionThroughInline(admin.TabularInline):
    model = AssignmentQuestionThrough
    extra = 1


# Inline for new Question creation in Assignment form
class AssignmentQuestionInline(admin.StackedInline):
    model = AssignmentQuestion
    form = AssignmentQuestionInlineForm
    extra = 1

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(teacher__user=request.user)

    def has_delete_permission(self, request, obj=None):
        return True


@admin.register(Assignment)
class AssignmentAdmin(admin.ModelAdmin):
    form = AssignmentAdminForm
    list_display = ('title', 'assigned_to', 'assigned_by', 'due_date')
    list_filter = ('assigned_to', 'assigned_by')
    search_fields = ('title',)
    filter_horizontal = ('questions',)
    inlines = [AssignmentQuestionThroughInline]

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(assigned_by__user=request.user)

    def save_model(self, request, obj, form, change):
        if not request.user.is_superuser and not obj.assigned_by_id:
            obj.assigned_by = request.user.teacher
        # Questions are validated in the form, exclude M2M from model validation
        obj.full_clean(exclude=['questions'])
        super().save_model(request, obj, form, change)


@admin.register(AssignmentQuestion)
class AssignmentQuestionAdmin(admin.ModelAdmin):
    list_display = ('text', 'teacher', 'marks', 'question_type', 'created_at')
    list_filter = ('teacher', 'question_type')
    search_fields = ('text',)

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if not request.user.is_superuser:
            qs = qs.filter(teacher__user=request.user)
        return qs

    def save_model(self, request, obj, form, change):
        if not request.user.is_superuser and not obj.teacher_id:
            obj.teacher = request.user.teacher
        obj.full_clean()
        super().save_model(request, obj, form, change)


class AnswerInline(admin.TabularInline):
    model = Answer
    extra = 0
    readonly_fields = ('question', 'selected_option', 'answer_text', 'is_correct', 'marks_awarded')
    can_delete = False


@admin.register(AssignmentAttempt)
class AssignmentAttemptAdmin(admin.ModelAdmin):
    list_display = ('student', 'assignment', 'is_submitted', 'submitted_at')
    list_filter = ('is_submitted', 'assignment')
    search_fields = ('student__name', 'assignment__title')
    inlines = [AnswerInline]
