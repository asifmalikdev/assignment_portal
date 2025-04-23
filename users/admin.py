from django.contrib import admin
from .models import UserProfile, StudentProfile, TeacherProfile

admin.site.register(UserProfile)
admin.site.register(StudentProfile)
admin.site.register(TeacherProfile)