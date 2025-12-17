from django.db import models


class Course(models.Model):
	DEPARTMENT_CHOICES = [
		("CS", "Computer Science"),
		("MATH", "Mathematics"),
		("ENG", "Engineering"),
		("BUS", "Business"),
		("SCI", "Science"),
		("ART", "Arts"),
		("MED", "Medicine"),
		("LAW", "Law"),
		("EDU", "Education"),
		("OTHER", "Other"),
	]

	code = models.CharField(max_length=20, unique=True)
	title = models.CharField(max_length=200)
	description = models.TextField(blank=True)
	credits = models.PositiveIntegerField(default=3)
	# Matches migration 0002_course_department
	department = models.CharField(max_length=10, choices=DEPARTMENT_CHOICES, default="OTHER")
	created_at = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return f"{self.code} - {self.title}"
