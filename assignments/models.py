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


    def clean(self):
        if self.assigned_by and self.assigned_to:
            if not self.assigned_by.assigned_classes.filter(pk=self.assigned_to.pk).exists():
                raise ValidationError("Teacher is Not Assigned to this class")
    def __str__(self):
        return f"{self.title} - {self.assigned_to.name}"






def submission_file_path(instance, filename):
    return f'submissions/class_{instance.assignment.assigned_to.id}/assignment_{instance.assignment.id}/student_{instance.submitted_by.id}/{filename}'


class Submission(models.Model):
    id = models.AutoField(primary_key=True)
    assignment = models.ForeignKey(Assignment, on_delete=models.CASCADE, related_name='submissions')
    submitted_by = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='submissions')
    submitted_at = models.DateTimeField(auto_now_add=True)
    file = models.FileField(upload_to=submission_file_path)
    comment = models.TextField(blank=True, null=True)

    class Meta:
        unique_together = ('assignment', 'submitted_by')  # Prevent multiple submissions

    def clean(self):
        errors = {}

        if self.assignment and self.submitted_by:
            student_class = self.submitted_by.student_class
            if student_class != self.assignment.assigned_to:
                errors['submitted_by'] = "This student does not belong to the class this assignment was assigned to."

        # Validate: Submission must be before due date
        if self.assignment and self.assignment.due_date < timezone.now().date():
            errors['assignment'] = "This assignment's due date has passed. Submission not allowed."

        # Validate: File is required
        if not self.file:
            errors['file'] = "A file must be uploaded with the submission."

        if errors:
            raise ValidationError(errors)

    def __str__(self):
        return f"{self.assignment.title} - {self.submitted_by.name}"










