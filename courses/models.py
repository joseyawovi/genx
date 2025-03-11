from django.db import models
from django.contrib.auth.models import User

class Instructor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(blank=True, null=True)
    profile_image = models.ImageField(upload_to='instructors/', blank=True, null=True)

    def __str__(self):
        return self.user.get_full_name() or self.user.username

class Course(models.Model):
    title = models.CharField(max_length=200)
    description = models.CharField(max_length=300)
    cover_image = models.ImageField(upload_to='courses/' ,blank=True, null=True)
    instructor = models.ForeignKey(Instructor, on_delete=models.CASCADE)
    lessons = models.PositiveIntegerField(default=0)
    students_enrolled = models.PositiveIntegerField(default=0)
    is_live = models.BooleanField(default=False)
    is_free = models.BooleanField(default=False)

    def __str__(self):
        return self.title
