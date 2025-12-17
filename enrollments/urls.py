from django.urls import path
from . import views

app_name = 'enrollments'

urlpatterns = [
    path('', views.EnrollmentListView.as_view(), name='list'),
    path('create/', views.EnrollmentCreateView.as_view(), name='create'),
    path('<int:pk>/', views.EnrollmentDetailView.as_view(), name='detail'),
    path('<int:pk>/update/', views.EnrollmentUpdateView.as_view(), name='update'),
    path('<int:pk>/delete/', views.EnrollmentDeleteView.as_view(), name='delete'),
    path('transcript/<int:student_id>/', views.student_transcript, name='transcript'),
    path('course-report/<int:course_id>/', views.course_enrollment_report, name='course_report'),
]
