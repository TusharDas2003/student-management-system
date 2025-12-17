from django.shortcuts import render
from students.models import Student
from courses.models import Course
from enrollments.models import Enrollment

def home(request):
    stats = {
        'students': Student.objects.count(),
        'courses': Course.objects.count(),
        'enrollments': Enrollment.objects.count(),
    }
    return render(request, 'home.html', stats)
