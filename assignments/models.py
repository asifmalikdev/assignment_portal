from django.utils import timezone

from django.core.exceptions import ValidationError
from django.db import models
from django.db.models import CASCADE

from role.models import Class, Teacher, Student


def validate_due_date(value):
    if value<timezone.now().date():
        raise ValidationError("Due date can't be in past")


class Assignment(models.Model):
    id = models.AutoField(primary_key = True)
    title = models.CharField(max_length=255, verbose_name="Title ")
    description = models.TextField(verbose_name="Description")
    due_date = models.DateField(validators=[validate_due_date])
    created_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)
    assigned_by = models.ForeignKey(Teacher, on_delete=CASCADE, related_name="Assigner")
    assigned_to = models.ForeignKey(Class, on_delete=CASCADE, related_name="Assigned_Teacher")

    def __str__(self):
        return f"{self.title} - {self.assigned_to.name}"

class Submission(models.Model):
    assignment = models.ForeignKey(Assignment, on_delete=CASCADE, related_name="submissions")
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    file = models.FileField(upload_to="submissions/")
    submitted_at = models.DateTimeField(auto_now_add=True)
    marks = models.PositiveIntegerField(null=True, blank=True)

    def clean(self):
        if self.assignment and self.assignment.due_date < timezone.now().date():
            raise ValidationError("Submission is past the due date")
        if Submission.objects.filter(assignment=self.assignment, student=self.student).exclude(pk=self.pk).exists():
            raise ValidationError("You have already submited this file")

    def __str__(self):
        return f"{self.student.name}, {self.assignment.title}"












