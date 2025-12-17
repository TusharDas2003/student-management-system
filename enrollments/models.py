from django.db import models
from students.models import Student
from courses.models import Course

class Enrollment(models.Model):
	GRADE_CHOICES = [
		('A+', 'A+'),
		('A', 'A'),
		('A-', 'A-'),
		('B+', 'B+'),
		('B', 'B'),
		('B-', 'B-'),
		('C+', 'C+'),
		('C', 'C'),
		('C-', 'C-'),
		('D', 'D'),
		('F', 'F'),
		('IP', 'In Progress'),
		('W', 'Withdrawn'),
	]
	
	student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='enrollments')
	course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='enrollments')
	enrolled_on = models.DateField(auto_now_add=True)
	grade = models.CharField(max_length=3, choices=GRADE_CHOICES, blank=True, null=True)
	marks = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True, 
								help_text="Marks out of 100")

	class Meta:
		unique_together = ('student', 'course')

	def __str__(self):
		return f"{self.student} -> {self.course}"
	
	def get_grade_display_with_marks(self):
		if self.marks and self.grade:
			return f"{self.grade} ({self.marks}%)"
		elif self.grade:
			return self.grade
		elif self.marks:
			return f"{self.marks}%"
		return "Not graded"
