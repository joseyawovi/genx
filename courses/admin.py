from django.contrib import admin
from .models import  *

admin.site.register(Course)
admin.site.register(Instructor)
admin.site.register(Module)
admin.site.register(Lesson)
admin.site.register(Enrollment)