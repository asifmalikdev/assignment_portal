from django.db import models
from django.contrib.auth.models import User


class District(models.Model):
    name=models.CharField(max_length=100)

    def __str__(self):
        return self.name
class School(models.Model):
    name = models.CharField(max_length=100)
    district = models.ForeignKey(District, on_delete=models.CASCADE, related_name='schools')

    def __str__(self):
        return f"{self.name} ({self.district.name})"


class SchoolClass(models.Model):
    CLASS_CHOICES = [
        ('8','8th Grade'),
        ('9', '9th Grade'),
        ('10', '10th Grade'),
    ]
    name = models.CharField(max_length=10, choices=CLASS_CHOICES)
    school = models.ForeignKey(School, on_delete=models.CASCADE, related_name="classes")

    def __str__(self):
        return f"{self.school.name} - {self.get_name_display()}"
