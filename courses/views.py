from django.shortcuts import render, get_object_or_404
from .models import Course, Instructor

def course_list(request):
    courses = Course.objects.all()
    return render(request, 'courses/course_list.html', {'courses': courses})

# Course Detail View
def course_detail(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    return render(request, 'courses/course_detail.html', {'course': course})

# Instructor Profile View
def instructor_profile(request, instructor_id):
    instructor = get_object_or_404(Instructor, id=instructor_id)
    return render(request, 'courses/instructor_profile.html', {'instructor': instructor})
