from django.shortcuts import render, get_object_or_404, redirect
from .models import Course, Module, Instructor, Enrollment,Lesson
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from reportlab.pdfgen import canvas
from io import BytesIO
from reportlab.lib.pagesizes import letter
from reportlab.lib.utils import ImageReader

def course_list(request):
    courses = Course.objects.all()
    return render(request, 'courses/course_list.html', {'courses': courses})

def course_detail(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    modules = course.modules.all().order_by('order')  # Fetch modules for the course
    return render(request, 'courses/course_detail.html', {
        'course': course,
        'modules': modules,
    })

# Instructor Profile View
def instructor_profile(request, instructor_id):
    instructor = get_object_or_404(Instructor, id=instructor_id)
    return render(request, 'courses/instructor_profile.html', {'instructor': instructor})



@login_required
@login_required
def enroll_course(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    # Check if the user is already enrolled
    if not Enrollment.objects.filter(user=request.user, course=course).exists():
        Enrollment.objects.create(user=request.user, course=course)
    return redirect('dashboard')  # Redirect to the general dashboard

from django.shortcuts import get_object_or_404, render
from django.contrib.auth.decorators import login_required
from .models import Lesson, Enrollment

@login_required
def lesson_detail(request, lesson_id):
    lesson = get_object_or_404(Lesson, id=lesson_id)
    enrollment = get_object_or_404(Enrollment, user=request.user, course=lesson.module.course)

    # Get all lessons in the course
    lessons = Lesson.objects.filter(module__course=lesson.module.course).order_by('module__order', 'order')

    # Find the current lesson's position
    lesson_list = list(lessons)
    current_index = lesson_list.index(lesson)

    # Get previous and next lessons
    previous_lesson = lesson_list[current_index - 1] if current_index > 0 else None
    next_lesson = lesson_list[current_index + 1] if current_index < len(lesson_list) - 1 else None

    # Fetch completed lesson IDs
    completed_lesson_ids = enrollment.completed_lessons.values_list('id', flat=True)

    return render(request, 'courses/lesson_detail.html', {
        'lesson': lesson,
        'enrollment': enrollment,
        'previous_lesson': previous_lesson,
        'next_lesson': next_lesson,
        'completed_lesson_ids': completed_lesson_ids,  # Pass completed lesson IDs to the template
    })

@login_required
def dashboard(request):
    enrollments = Enrollment.objects.filter(user=request.user).select_related('course')
    return render(request, 'courses/dashboard.html', {'enrollments': enrollments})


@login_required
def mark_lesson_completed(request, lesson_id):
    lesson = get_object_or_404(Lesson, id=lesson_id)
    enrollment = get_object_or_404(Enrollment, user=request.user, course=lesson.module.course)
    enrollment.completed_lessons.add(lesson)

    # Get all lessons in the course
    lessons = Lesson.objects.filter(module__course=lesson.module.course).order_by('module__order', 'order')

    # Find the current lesson's position
    lesson_list = list(lessons)
    current_index = lesson_list.index(lesson)

    # Check if the course is completed
    if enrollment.is_course_completed:
        # Redirect to the last lesson to show the completion message
        return redirect('lesson_detail', lesson_id=lesson.id)
    elif current_index < len(lesson_list) - 1:
        # Redirect to the next lesson
        next_lesson = lesson_list[current_index + 1]
        return redirect('lesson_detail', lesson_id=next_lesson.id)
    else:
        # No more lessons, redirect to dashboard
        return redirect('dashboard')


@login_required
def generate_certificate(request, course_id):
    enrollment = get_object_or_404(Enrollment, user=request.user, course_id=course_id)
    if not enrollment.is_course_completed:
        return HttpResponse("You have not completed this course yet.", status=403)

    # Create a PDF certificate
    buffer = BytesIO()
    p = canvas.Canvas(buffer, pagesize=letter)
    width, height = letter

    # Add a logo
    logo = ImageReader('static/assets/img/logo/logo-1.png')
    p.drawImage(logo, 100, height - 150, width=100, height=100)

    # Add text
    p.setFont("Helvetica-Bold", 24)
    p.drawString(100, height - 200, "Certificate of Completion")
    p.setFont("Helvetica", 18)
    p.drawString(100, height - 250, f"This certifies that {request.user.username} has successfully completed the course:")
    p.drawString(100, height - 300, f"'{enrollment.course.title}'")
    p.drawString(100, height - 350, f"on {enrollment.course.created_at.strftime('%Y-%m-%d')}.")
    p.showPage()
    p.save()

    # Prepare the response
    buffer.seek(0)
    response = HttpResponse(buffer, content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="certificate_{enrollment.course.title}.pdf"'
    return response