from django.utils import timezone
from django.core.exceptions import ValidationError
from django.db import models
from django.db.models import CASCADE
from role.models import Class, Teacher, Student


# ------------------ VALIDATORS ------------------

def validate_due_date(value):
    if value < timezone.now().date():
        raise ValidationError("Due date can't be in the past.")


# ------------------ ASSIGNMENT ------------------

class Assignment(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=255, verbose_name="Title")
    description = models.TextField(verbose_name="Description")
    due_date = models.DateField(validators=[validate_due_date])
    created_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    # Previously you stored assignment_type here. Removed — now handled per question.
    assigned_by = models.ForeignKey(Teacher, on_delete=CASCADE, related_name="assigned_assignments")
    assigned_to = models.ForeignKey(Class, on_delete=CASCADE, related_name="class_assignments")

    def clean(self):
        if self.assigned_by_id and self.assigned_to_id:
            if not self.assigned_by.assigned_classes.filter(pk=self.assigned_to.pk).exists():
                raise ValidationError("This teacher is not assigned to the selected class.")

    def __str__(self):
        return f"{self.title} - {self.assigned_to.name}"


class AssignmentQuestion(models.Model):
    QUESTION_TYPE_CHOICES = [
        ('MCQ', 'Multiple Choice'),
        ('DESC', 'Descriptive'),
    ]

    assignment = models.ForeignKey(Assignment, on_delete=models.CASCADE, related_name='questions')
    question_type = models.CharField(max_length=4, choices=QUESTION_TYPE_CHOICES)
    question_text = models.TextField()
    marks = models.PositiveIntegerField()

    # MCQ fields (optional if not MCQ)
    option_a = models.CharField(max_length=255, blank=True, null=True)
    option_b = models.CharField(max_length=255, blank=True, null=True)
    option_c = models.CharField(max_length=255, blank=True, null=True)
    option_d = models.CharField(max_length=255, blank=True, null=True)
    correct_option = models.CharField(
        max_length=1,
        choices=[('a', 'A'), ('b', 'B'), ('c', 'C'), ('d', 'D')],
        blank=True,
        null=True
    )

    def clean(self):
        if self.question_type == 'MCQ':
            if not all([self.option_a, self.option_b, self.option_c, self.option_d, self.correct_option]):
                raise ValidationError("All options and the correct answer must be provided for an MCQ question.")
        elif self.question_type == 'DESC':
            if any([self.option_a, self.option_b, self.option_c, self.option_d, self.correct_option]):
                raise ValidationError("Descriptive questions should not have options or correct answer.")

    def __str__(self):
        return f"{self.get_question_type_display()}: {self.question_text[:50]}"
def submission_file_path(instance, filename):
    return f'submissions/class_{instance.assignment.assigned_to.id}/assignment_{instance.assignment.id}/student_{instance.submitted_by.id}/{filename}'


class Submission(models.Model):
    id = models.AutoField(primary_key=True)
    assignment = models.ForeignKey(Assignment, on_delete=CASCADE, related_name='submissions')
    submitted_by = models.ForeignKey(Student, on_delete=CASCADE, related_name='submissions')
    submitted_at = models.DateTimeField(auto_now_add=True)
    file = models.FileField(upload_to=submission_file_path)
    comment = models.TextField(blank=True, null=True)

    class Meta:
        unique_together = ('assignment', 'submitted_by')  # One submission per student per assignment

    def clean(self):
        errors = {}

        # Validate: Student must belong to the assigned class
        if self.assignment_id and self.submitted_by_id:
            student_class_id = self.submitted_by.student_class_id
            assigned_class_id = self.assignment.assigned_to_id
            if student_class_id != assigned_class_id:
                errors['submitted_by'] = "This student does not belong to the class this assignment is assigned to."

        # Validate: Submission must be before due date
        if self.assignment_id and self.assignment.due_date < timezone.now().date():
            errors['assignment'] = "This assignment's due date has passed. Submission not allowed."

        # Validate: File must be uploaded
        if not self.file:
            errors['file'] = "A file must be uploaded with the submission."

        if errors:
            raise ValidationError(errors)

    def __str__(self):
        return f"{self.assignment.title} - {self.submitted_by.name}"
