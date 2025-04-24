from django.contrib import admin
from django import forms
from .models import Role, District, School, Class, Teacher, Student
from .forms import TeacherForm


@admin.register(Role)
class RoleAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', "create_time", 'is_active')
    list_filter = ('is_active',)
    search_fields = ('name',)
    ordering = ('create_time',)
    list_display_links = ('name',)


@admin.register(District)
class DistrictAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'create_time', 'is_active')
    list_filter = ('is_active',)
    search_fields = ('name',)
    ordering = ('create_time',)


@admin.register(School)
class SchoolAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'district', 'created_at', 'is_active')
    list_filter = ('district', 'is_active')
    search_fields = ('name', 'district__name')
    ordering = ('created_at',)
    list_display_links = ('name',)


@admin.register(Class)
class ClassAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'grade_level', 'school', 'is_active',)
    list_filter = ('grade_level', 'school', 'is_active')
    ordering = ('created_at',)


@admin.register(Teacher)
class TeacherAdmin(admin.ModelAdmin):
    form = TeacherForm
    list_display = ('id', 'name', 'email', 'subject', 'is_active', 'get_assigned_classes')

    class Media:
        js = ('admin/js/teacher_form.js',)  # Load custom JS

    def get_queryset(self, request):
        return super().get_queryset(request).prefetch_related('assigned_classes')

    def get_assigned_classes(self, obj):
        return ", ".join([f"{cls.name} ({cls.school.name})" for cls in obj.assigned_classes.all()])
    get_assigned_classes.short_description = 'Assigned Classes'
    get_assigned_classes.admin_order_field = None


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'email', 'address', 'school', 'student_class', 'is_active')
    list_filter = ('school', 'student_class', 'is_active',)
    readonly_fields = ('created_at',)
    search_fields = ('id', 'name', 'email', 'school',)

    fieldsets = (
        ("Student Information", {
            "fields": ('id', 'name', 'email', 'address')
        }),
        ("Academic Info", {
            'fields': ('school', 'student_class')
        }),
        ("Status", {
            'fields': ('is_active',)
        }),
    )
