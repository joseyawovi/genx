from django.db import models
from django.contrib.auth.models import User

class Instructor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(blank=True, null=True)
    profile_image = models.ImageField(upload_to='instructors/', blank=True, null=True)

    def __str__(self):
        return self.user.get_full_name() or self.user.username

from django.db import models
from django.contrib.auth.models import User

class Course(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    image = models.ImageField(upload_to='course_images/')
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    is_free = models.BooleanField(default=False)
    instructor = models.ForeignKey(Instructor, on_delete=models.CASCADE, related_name='courses_taught')
    category = models.CharField(max_length=100, default='Web Development')
    created_at = models.DateTimeField(auto_now_add=True)
    learning_outcomes = models.TextField(default='What you will learn...')
    total_lessons = models.PositiveIntegerField(default=0)
    total_duration = models.CharField(max_length=50, default='15h 30m 36s')
    level = models.CharField(max_length=50, default='Beginner')
    language = models.CharField(max_length=50, default='English')
    total_quizzes = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.title

class Module(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='modules')
    title = models.CharField(max_length=200)
    order = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.title

class Lesson(models.Model):
    module = models.ForeignKey(Module, on_delete=models.CASCADE, related_name='lessons')
    title = models.CharField(max_length=200)
    youtube_video_id = models.CharField(max_length=100, help_text="Enter the YouTube video ID (e.g., 'dQw4w9WgXcQ').")
    duration = models.CharField(max_length=50, default='10m', help_text="Duration of the lesson (e.g., '10m', '1h 30m').")
    order = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.title

class Enrollment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='enrollments')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='enrollments')
    enrolled_at = models.DateTimeField(auto_now_add=True)
    completed_lessons = models.ManyToManyField(Lesson, blank=True)

    @property
    def progress(self):
        total_lessons = self.course.modules.aggregate(total=models.Count('lessons'))['total']
        completed_lessons = self.completed_lessons.count()
        return int((completed_lessons / total_lessons) * 100) if total_lessons > 0 else 0
    
    @property
    def is_course_completed(self):
        total_lessons = self.course.modules.aggregate(total=models.Count('lessons'))['total']
        completed_lessons = self.completed_lessons.count()
        return completed_lessons >= total_lessons

   