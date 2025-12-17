from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.db.models import Q, Avg
from django.contrib import messages
from django.http import HttpResponse
from django.template.loader import render_to_string
from .models import Enrollment
from .forms import EnrollmentForm, EnrollmentGradeForm
from students.models import Student


class EnrollmentListView(ListView):
    model = Enrollment
    template_name = 'enrollments/list.html'
    context_object_name = 'enrollments'
    paginate_by = 15

    def get_queryset(self):
        queryset = Enrollment.objects.select_related('student', 'course')
        
        # Search functionality
        query = self.request.GET.get('q', '')
        if query:
            queryset = queryset.filter(
                Q(student__first_name__icontains=query) |
                Q(student__last_name__icontains=query) |
                Q(course__code__icontains=query) |
                Q(course__title__icontains=query)
            )
        
        # Filter by grade
        grade_filter = self.request.GET.get('grade', '')
        if grade_filter:
            queryset = queryset.filter(grade=grade_filter)
        
        # Filter by student
        student_filter = self.request.GET.get('student', '')
        if student_filter:
            try:
                queryset = queryset.filter(student_id=int(student_filter))
            except ValueError:
                pass
        
        # Sorting
        sort = self.request.GET.get('sort', '-enrolled_on')
        queryset = queryset.order_by(sort)
        
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['query'] = self.request.GET.get('q', '')
        context['grade_filter'] = self.request.GET.get('grade', '')
        context['student_filter'] = self.request.GET.get('student', '')
        context['sort'] = self.request.GET.get('sort', '-enrolled_on')
        context['grade_choices'] = Enrollment.GRADE_CHOICES
        return context


class EnrollmentDetailView(DetailView):
    model = Enrollment
    template_name = 'enrollments/detail.html'
    context_object_name = 'enrollment'


class EnrollmentCreateView(CreateView):
    model = Enrollment
    form_class = EnrollmentForm
    template_name = 'enrollments/create.html'
    success_url = reverse_lazy('enrollments:list')

    def form_valid(self, form):
        messages.success(self.request, 'Enrollment created successfully!')
        return super().form_valid(form)


class EnrollmentUpdateView(UpdateView):
    model = Enrollment
    form_class = EnrollmentGradeForm
    template_name = 'enrollments/update.html'
    success_url = reverse_lazy('enrollments:list')

    def form_valid(self, form):
        messages.success(self.request, 'Enrollment updated successfully!')
        return super().form_valid(form)


class EnrollmentDeleteView(DeleteView):
    model = Enrollment
    template_name = 'enrollments/delete.html'
    success_url = reverse_lazy('enrollments:list')

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, 'Enrollment deleted successfully!')
        return super().delete(request, *args, **kwargs)


def student_transcript(request, student_id):
    """Generate a transcript for a student"""
    student = get_object_or_404(Student, pk=student_id)
    enrollments = student.enrollments.select_related('course').order_by('-enrolled_on')
    
    # Calculate statistics
    graded_enrollments = enrollments.exclude(marks__isnull=True)
    avg_marks = graded_enrollments.aggregate(Avg('marks'))['marks__avg']
    total_credits = sum(e.course.credits for e in enrollments)
    
    context = {
        'student': student,
        'enrollments': enrollments,
        'avg_marks': avg_marks,
        'total_credits': total_credits,
    }
    
    if request.GET.get('format') == 'pdf':
        # For PDF generation, you'd need a library like ReportLab or WeasyPrint
        messages.info(request, 'PDF generation not yet implemented. Showing HTML version.')
    
    return render(request, 'enrollments/transcript.html', context)


def course_enrollment_report(request, course_id):
    """Generate enrollment report for a course"""
    from courses.models import Course
    course = get_object_or_404(Course, pk=course_id)
    enrollments = course.enrollments.select_related('student').order_by('student__last_name', 'student__first_name')
    
    # Calculate statistics
    total_enrolled = enrollments.count()
    graded_enrollments = enrollments.exclude(marks__isnull=True)
    avg_marks = graded_enrollments.aggregate(Avg('marks'))['marks__avg']
    
    context = {
        'course': course,
        'enrollments': enrollments,
        'total_enrolled': total_enrolled,
        'avg_marks': avg_marks,
    }
    
    return render(request, 'enrollments/course_report.html', context)
