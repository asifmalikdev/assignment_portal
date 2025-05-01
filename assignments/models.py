from django.utils import timezone
from django.core.exceptions import ValidationError
from django.db import models
from django.db.models import CASCADE
from role.models import Class, Teacher, Student
from django.contrib import admin


# ------------------ VALIDATORS ------------------

def validate_due_date(value):
    if value < timezone.now().date():
        raise ValidationError("Due date can't be in the past.")



class AssignmentQuestion(models.Model):
    QUESTION_TYPE_CHOICES = [
        ('LONG', 'Long Question'),
        ('SHORT', 'Short Question'),
        ('MCQ', 'Multiple Choice'),
    ]
    teacher = models.ForeignKey(Teacher, on_delete=CASCADE,related_name='questions')
    assigned_class = models.ForeignKey(Class, on_delete=CASCADE, related_name='questions',)
    question_type = models.CharField(max_length=5, choices=QUESTION_TYPE_CHOICES)
    text = models.TextField()
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
    created_at = models.DateTimeField(auto_now_add=True)


    def clean(self):
        if self.question_type == 'MCQ':
            if not all([self.option_a, self.option_b, self.option_c, self.option_d, self.correct_option]):
                raise ValidationError("All options and the correct answer must be provided for an MCQ question.")
        else:
            if any([self.option_a, self.option_b, self.option_c, self.option_d, self.correct_option]):
                raise ValidationError('Options are only allowed for MCQ')
        if not self.teacher.assigned_classes.filter(pk=self.assigned_class.pk).exists():
            raise ValidationError("This teacher is not assigned to the selected class.")

    def __str__(self):
        return f"{self.get_question_type_display()}: {self.text}"


from django.db import transaction
class Assignment(models.Model):
    title = models.CharField(max_length=255, verbose_name="Title")
    description = models.TextField(verbose_name="Description", blank=True)
    due_date = models.DateField(validators=[validate_due_date])
    created_at = models.DateTimeField(auto_now_add=True)
    assigned_by = models.ForeignKey(Teacher, on_delete=CASCADE, related_name="assigned_assignments")
    assigned_to = models.ForeignKey(Class, on_delete=CASCADE, related_name="class_assignments")
    questions = models.ManyToManyField(
        AssignmentQuestion,
        through='AssignmentQuestionThrough',
        related_name='assignments')


    def clean(self):
        print('but hameed is here not asif')

        if self.assigned_by and self.assigned_to:
            if not self.assigned_by.assigned_classes.filter(pk=self.assigned_to.pk).exists():
                raise ValidationError("This teacher is not assigned to the selected class.")

        # print('hello asif i am here -------------\n----------------\n------------\n-------------\n')
        # invalid_questions = self.questions.exclude(teacher=self.assigned_by)
        # if invalid_questions.exists():
        #     raise ValidationError("One or More Questions are not from Question book of this teacher")
        # invalid_questions_for_class = self.questions.exclude(assigned_class= self.assigned_to)
        # print("debuger ---------------------------------------\n")
        # if invalid_questions_for_class.exists():
        #     raise ValidationError("one or more question are not for this class")


    def __str__(self):
        return f"{self.title} for {self.assigned_to.name} by {self.assigned_by.name} "

    def save(self, *args, **kwargs):
        self.full_clean()
        with transaction.atomic():
            super().save(*args, **kwargs)

            invalid_questions = self.questions.exclude(teacher = self.assigned_by)
            if invalid_questions:
                raise ValidationError("one or more questions are not from this teacher's question book")

            invalid_class_questions = self.questions.exclude(assigned_class = self.assigned_to)
            if invalid_class_questions.exists():
                raise ValidationError("one or more questions are not intended for this class")

class AssignmentQuestionThrough(models.Model):
    assignment = models.ForeignKey(Assignment, on_delete=models.CASCADE, related_name='question_links')
    question = models.ForeignKey(AssignmentQuestion, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('assignment', 'question')

class AssignmentAttempt(models.Model):
    student = models.ForeignKey(Student, on_delete=CASCADE, related_name='assignment_attempts')
    assignment = models.ForeignKey(Assignment, on_delete=CASCADE, related_name='attempt')
    started_at  = models.DateTimeField(auto_now_add=True)
    submitted_at = models.DateTimeField(null=True, blank=True)
    is_submitted = models.BooleanField(default=False)
    class Meta:
        unique_together = ('student', 'assignment')
    def __str__(self):
        return f'{self.student.name}  → {self.assignment.title}'

class Answer(models.Model):
    attempt = models.ForeignKey(AssignmentAttempt, on_delete=CASCADE, related_name="answers")
    question = models.ForeignKey(AssignmentQuestion, on_delete=CASCADE)
    selected_option = models.CharField(
        max_length=1,
        choices=[('a', 'A'), ('b', 'B'), ('c', 'C'), ('d', 'D')],
        blank = True,
        null=True
    )
    answer_text = models.TextField(blank=True, null=True)

    is_correct = models.BooleanField(null=True, blank=True)
    marks_awarded = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)

    class Meta:
        unique_together = ('attempt', 'question')
    def auto_mark(self):
        if self.question_type == 'MCQ':
            self.is_correct = self.selected_option == self.question.correct_option
            self.marks_awarded = self.question.marks if self.is_correct else 0
    def __str__(self):
        return f"{self.attempt.student.name}'s answer to Q{self.question.id}"
