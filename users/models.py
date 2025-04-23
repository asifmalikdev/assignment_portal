from django.db import models
from django.contrib.auth.models import User
from schools.models import School, SchoolClass
from subjects.models import Subject


class UserProfile(models.Model):
    ROLE_CHOICE = (
        ('student', 'Student'),
        ('teacher', 'Teacher'),
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    role = models.CharField(max_length=10, choices=ROLE_CHOICE)
    phone = models.CharField(max_length=15, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.username

class TeacherProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='teacher_profile')
    school = models.ForeignKey(School, on_delete=models.CASCADE, related_name='teachers')
    subjects = models.ManyToManyField(Subject)
    classes = models.ManyToManyField(SchoolClass)

    def __str__(self):
        return f"Teacher: {self.user.username}"


class StudentProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='student_profile')
    classroom = models.ForeignKey(SchoolClass, on_delete=models.CASCADE, related_name='students')

    def __str__(self):
        return f"Student: {self.user.username}"







