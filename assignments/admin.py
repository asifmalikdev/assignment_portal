from django.contrib import admin
from django.core.exceptions import ValidationError
from .forms import AssignmentForm
from .models import Assignment, AssignmentQuestion, Submission

@admin.register(AssignmentQuestion)
class AssignmentQuestionAdmin(admin.ModelAdmin):
    list_display = ('text', 'teacher', 'marks', 'question_type', 'created_at')
    list_filter = ('teacher', 'question_type')
    search_fields = ('text',)

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if not request.user.is_superuser:
            qs = qs.filter(teacher__email=request.user.email)
        return qs

    def save_model(self, request, obj, form, change):
        if not request.user.is_superuser and not obj.teacher_id:
            obj.teacher = request.user.teacher
        obj.full_clean()
        super().save_model(request, obj, form, change)


class AttachExistingQuestionInline(admin.TabularInline):
    model = Assignment.questions.through
    extra = 1
    verbose_name = "Attach Question"
    verbose_name_plural = "Attach Questions from Question Book"

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'assignmentquestion' and not request.user.is_superuser:
            kwargs['queryset'] = AssignmentQuestion.objects.filter(teacher__email=request.user.email)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)




@admin.register(Assignment)
class AssignmentAdmin(admin.ModelAdmin):
    form = AssignmentForm  # still using this for validation

    def formfield_for_manytomany(self, db_field, request, **kwargs):
        if db_field.name == "questions":
            if request.user.is_superuser:
                kwargs["queryset"] = AssignmentQuestion.objects.all()
            else:
                kwargs["queryset"] = AssignmentQuestion.objects.filter(teacher=request.user)
        return super().formfield_for_manytomany(db_field, request, **kwargs)


@admin.register(Submission)
class SubmissionAdmin(admin.ModelAdmin):
    list_display = ('assignment', 'submitted_by', 'submitted_at')
    list_filter = ('assignment__assigned_to', 'assignment', 'submitted_at')
    search_fields = ('assignment__title', 'submitted_by__name')


























































# from django.contrib import admin
# from .models import Assignment, AssignmentQuestion, Submission
#
# # @admin.register(AssignmentQuestion)
# class AssignmentQuestionInline(admin.StackedInline):
#     model = Assignment.questions.through
#     extra = 1  # Show 1 empty row by default
#     verbose_name = "Attach Existing Questions"
#     verbose_name_plural = "Questions"
#
#
# @admin.register(Assignment)
# class AssignmentAdmin(admin.ModelAdmin):
#     inlines = [AssignmentQuestionInline]
#     filter_horizontal = ('questions',)
#     list_display = ('title','assigned_by', 'assigned_to',  'due_date', 'created_at')
#     def formfield_for_manytomany(self, db_field, request, **kwargs):
#         if db_field.name == 'questions' and request.user.is_superuser is False:
#             kwargs["queryset"]=AssignmentQuestion.objects.filter(teacher__email = request.user.email)
#
#         return super().formfield_for_manytomany(db_field, request, **kwargs)
#
#
# class NewQuestionInline(admin.StackedInline):
#     model = AssignmentQuestion
#     extra = 1
#     verbose_name = 'New Question'
#     verbose_name_plural = "Create New Question"
#     exclude = 'assignments'
#     show_change_link = True
#
#     def get_queryset(self, request):
#         return AssignmentQuestion.objects.none()
# class AttachExistingQuestionInline(admin.TabularInline):
#     model = Assignment.questions.through
#     extra = 1
#     verbose_name = 'Attach Question'
#     verbose_name_plural = "Attach Question from Question Book"
#
# class AssignmentAdmin(admin.ModelAdmin):
#     inlines = [AttachExistingQuestionInline, NewQuestionInline]
#     filter_horizontal = ('questions',)
#     list_display = ('title', 'assigned_by', 'assigned_to', 'due_date')
#     exclude = ('questions',)  # hide default M2M widget since we’re using inlines
#
# admin.site.register(AssignmentAdmin)
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
# @admin.register(Submission)
# class SubmissionAdmin(admin.ModelAdmin):
#     list_display = ('assignment', 'submitted_by', 'submitted_at')
#     list_filter = ('assignment__assigned_to', 'assignment', 'submitted_at')
#     search_fields = ('assignment__title', 'submitted_by__name')
