from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.db.models import Q, Count
from django.contrib import messages
from .models import Course
from .forms import CourseForm


class CourseListView(ListView):
    model = Course
    template_name = 'courses/list.html'
    context_object_name = 'courses'
    paginate_by = 10

    def get_queryset(self):
        queryset = Course.objects.all().annotate(enrollment_count=Count('enrollments'))
        
        # Search functionality
        query = self.request.GET.get('q', '')
        if query:
            queryset = queryset.filter(
                Q(code__icontains=query) |
                Q(title__icontains=query)
            )
        
        # Filter by credits
        credits_filter = self.request.GET.get('credits', '')
        if credits_filter:
            try:
                queryset = queryset.filter(credits=int(credits_filter))
            except ValueError:
                pass
        
        # Sorting
        sort = self.request.GET.get('sort', 'code')
        queryset = queryset.order_by(sort)
        
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['query'] = self.request.GET.get('q', '')
        context['credits_filter'] = self.request.GET.get('credits', '')
        context['sort'] = self.request.GET.get('sort', 'code')
        return context


class CourseDetailView(DetailView):
    model = Course
    template_name = 'courses/detail.html'
    context_object_name = 'course'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['enrollments'] = self.object.enrollments.select_related('student').order_by('-enrolled_on')
        return context


class CourseCreateView(CreateView):
    model = Course
    form_class = CourseForm
    template_name = 'courses/create.html'
    success_url = reverse_lazy('courses:list')

    def form_valid(self, form):
        messages.success(self.request, 'Course created successfully!')
        return super().form_valid(form)


class CourseUpdateView(UpdateView):
    model = Course
    form_class = CourseForm
    template_name = 'courses/update.html'
    success_url = reverse_lazy('courses:list')

    def form_valid(self, form):
        messages.success(self.request, 'Course updated successfully!')
        return super().form_valid(form)


class CourseDeleteView(DeleteView):
    model = Course
    template_name = 'courses/delete.html'
    success_url = reverse_lazy('courses:list')

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, 'Course deleted successfully!')
        return super().delete(request, *args, **kwargs)
