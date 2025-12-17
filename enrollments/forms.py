from django import forms
from .models import Enrollment
from students.models import Student
from courses.models import Course

class EnrollmentForm(forms.ModelForm):
    class Meta:
        model = Enrollment
        fields = ['student', 'course', 'grade', 'marks']
        widgets = {
            'student': forms.Select(attrs={'class': 'form-control'}),
            'course': forms.Select(attrs={'class': 'form-control'}),
            'grade': forms.Select(attrs={'class': 'form-control'}),
            'marks': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Marks (0-100)', 'step': '0.01'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['student'].queryset = Student.objects.all().order_by('last_name', 'first_name')
        self.fields['course'].queryset = Course.objects.all().order_by('code')
        self.fields['grade'].required = False
        self.fields['marks'].required = False


class EnrollmentGradeForm(forms.ModelForm):
    """Form for updating just the grade and marks of an enrollment"""
    class Meta:
        model = Enrollment
        fields = ['grade', 'marks']
        widgets = {
            'grade': forms.Select(attrs={'class': 'form-control'}),
            'marks': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Marks (0-100)', 'step': '0.01'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['grade'].required = False
        self.fields['marks'].required = False
