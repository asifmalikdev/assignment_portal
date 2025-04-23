from django.db import models
from django.db.models import CASCADE

from users.models import TeacherProfile, StudentProfile
from schools.models import SchoolClass
from subjects.models import Subject


class Assignment(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    teacher = models.ForeignKey(TeacherProfile, on_delete=models.CASCADE)
    classroom = models.ForeignKey(SchoolClass, on_delete=CASCADE)
    due_time = models.TimeField(default="23:59:00")  # ✅ ISO 8601 time string
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} ({self.classroom.name})"


class AssignmentSubmission(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('submitted', 'Submitted'),
        ('late', 'Late'),
    )
    student = models.ForeignKey(StudentProfile, on_delete=models.CASCADE)
    assignment = models.ForeignKey(Assignment, on_delete=CASCADE)
    submitted_file = models.FileField(upload_to='submissions/')
    submitted_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default="pending")

    def __str__(self):
        return f"{self.student.user.username} - {self.assignment.title}"



class AssignmentMark(models.Model):
    submission = models.OneToOneField(AssignmentSubmission, on_delete=models.CASCADE)
    marks = models.IntegerField()
    feedback = models.TextField(blank=True)
    marked_by = models.ForeignKey(TeacherProfile, on_delete=models.CASCADE)
    marked_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Marks for {self.submission.student.user.username} - {self.submission.assignment.title}"























