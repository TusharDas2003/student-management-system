from django.urls import path
from . import views

app_name = "analytics"

urlpatterns = [
    path("grades/", views.grade_analytics, name="grade_analytics"),
    path("student/<int:student_id>/", views.student_dashboard, name="student_dashboard"),
    path("departments/", views.department_reports, name="department_reports"),
]
