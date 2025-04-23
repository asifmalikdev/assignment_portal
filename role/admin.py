from PIL.PyAccess import mode_map
from django.contrib import admin
from .models import Role, District, School, Class, Teacher, Student


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
    list_display = ('id', 'name', 'grade_level','school', 'is_active',)
    list_filter = ('grade_level', 'school', 'is_active')
    ordering = ('created_at',)

@admin.register(Teacher)
class TeacherAdmin(admin.ModelAdmin):
    list_display = ('id','name','email','subject','get_assigned_classes', 'is_active', 'created_at')
    list_filter = ('is_active',)
    search_fields = ('name', 'email', 'subject')

    def get_assigned_classes(self, obj):
        return ", ".join([cls.name for cls in obj.assigned_classes.all()])

    get_assigned_classes.short_description = 'Assigned Classes'

@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'email', 'address', 'school', 'student_class','is_active')
    list_filter = ('school','student_class', 'is_active',)
    readonly_fields = ('created_at',)
    search_fields = ('id', 'name', 'email', 'school', )
    fieldsets = (
        ("Student Information",{
            "fields":('id', 'name', 'email' ,'address')
        }),
        ("Academic Info",{
            'fields': ('school', 'student_class')
        }),
        ("status",{
            'fields': ('is_active',)
        }),
    )


