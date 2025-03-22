from django.urls import path
from . import views

urlpatterns = [
    path('', views.course_list, name='course_list'),
    path('<int:course_id>/', views.course_detail, name='course_detail'),
    path('enroll/<int:course_id>/', views.enroll_course, name='enroll_course'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('lesson/<int:lesson_id>/', views.lesson_detail, name='lesson_detail'),
    path('mark-completed/<int:lesson_id>/', views.mark_lesson_completed, name='mark_lesson_completed'),
    path('generate-certificate/<int:course_id>/', views.generate_certificate, name='generate_certificate'),
]