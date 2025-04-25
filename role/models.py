import re
from django.db import models
from django.db.models import CASCADE
from django.core.exceptions import ValidationError
from numpy.ma.extras import unique


def validate_grade_level(value):
    if value < 1 or value > 12:
        raise ValidationError("Grade level must be between 1 and 12.")

class Role(models.Model):

    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255, unique=True, verbose_name="Role Name",
                            help_text="Enter a unique role name")
    create_time= models.DateTimeField(auto_now_add=True, verbose_name="Creater At")
    is_active = models.BooleanField(default = True, verbose_name="Is Active")

    def __str__(self):
        return self.name

    def clean(self):
        self.name = self.name.strip()
        self.name = self.name.lower()
        if not re.match(r'^[a-z\s]+$', self.name):
            raise ValidationError("role name must contains only lowercase letters and space")
        if len(self.name) < 4:
            raise ValidationError("Role name must be alteast 4 character")

class District(models.Model):
    id = models.AutoField(primary_key = True)
    name = models.CharField(max_length=255, unique=True, verbose_name="District Name")
    create_time = models.DateTimeField(auto_now_add=True, verbose_name="Created At")
    is_active = models.BooleanField(default=True, verbose_name="Is Active")
    def __str__(self):
        return self.name
    def clean(self):
        self.name = self.name.strip()
        self.name = self.name.lower()
        if len(self.name)<4:
            raise ValidationError("District name must contain atleast 4 character")
        if not re.match(r'^[a-z\s]+$', self.name):
            raise ValidationError("Name must contain letters only")


class School(models.Model):
    id = models.AutoField(primary_key = True)
    name = models.CharField(max_length=255, unique=True, verbose_name="School")
    address = models.TextField(verbose_name="Address")
    principal = models.CharField(max_length=255)
    district = models.ForeignKey(District, on_delete=CASCADE, related_name="school_district")
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True, verbose_name="Is Active")
    def __str__(self):
        return self.name
    def clean(self):
        self.name = self.name.strip().lower()
        if not re.match(r'^[a-zA-Z\s]+$', self.name):
            raise ValidationError("Only letter Please")
        if len(self.address.strip())<10:
            raise ValidationError("Address Must Contain Atleast 10 Character")

class Class(models.Model):
    name = models.CharField(max_length=100, verbose_name="Class Name")
    grade_level= models.IntegerField(validators=[validate_grade_level])
    school = models.ForeignKey(School, on_delete=CASCADE, related_name="School_Classes")
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True, verbose_name="Is Active")
    class Meta:
        unique_together = ('name', 'school')

    def clean(self):
        self.name = self.name.strip()

        if self.school and not self.school.is_active:
            raise ValidationError("Cannot assign class to an inactive school.")

        if len(self.name) < 2:
            raise ValidationError("Class name must be at least 2 characters long.")

    def __str__(self):
        return f"{self.name} - Grade {self.grade_level} ({self.school.name})"

class Teacher(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100, verbose_name="Teacher name")
    email = models.EmailField()
    subject = models.CharField(max_length=255)
    school = models.ForeignKey(School, on_delete=CASCADE, related_name="School_Teacher")
    assigned_classes = models.ManyToManyField(Class, related_name="class_teacher")  # fixed name here
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True, verbose_name="Is Active")

    def __str__(self):
        return f"{self.name} - {self.email}"

    def clean(self):
        self.name = self.name.strip()
        if len(self.name) < 3:
            raise ValidationError("Teacher name must contain at least 3 characters.")
        if not re.match(r'^[a-zA-Z\s]+$', self.name):
            raise ValidationError("Name can contain only letters and spaces.")




from django.core.validators import RegexValidator
class Student(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=255, verbose_name="student Name", validators=[RegexValidator(r'^[a-zA-Z\s]+$', message="Name must contain only letters and spaces.")])
    email = models.EmailField(unique=True)
    address = models.TextField()
    school = models.ForeignKey(School, on_delete=CASCADE, related_name="student")
    student_class = models.ForeignKey(Class, on_delete=CASCADE, related_name='students')

    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default= True, verbose_name='Is Active')

    def __str__(self):
        return f"{self.name}-{self.student_class.name} ({self.school.name})"
    def clean(self):
        self.name = self.name.strip()
        self.address = self.address.strip()
        if len(self.name)<3:
            raise ValidationError("Student Name Must Have Atleast 3 Letters")
        if len(self.address)<10:
            raise ValidationError("Address Must Contain Atleast 10 Characters")
        if not self.school.is_active:
            raise ValidationError("Cannot Assign Student to inactive school")
        if not self.student_class.is_active:

            raise ValidationError("Cannot Assign Student to inactive class")
        if self.student_class.school != self.school:
            raise ValidationError("Class does not belong to the selected school.")







