from django.db.models import Count, Avg, Q, Case, When, IntegerField
from django.shortcuts import render, get_object_or_404
from enrollments.models import Enrollment
from students.models import Student
from courses.models import Course

PASSING_GRADES = {"A+","A","A-","B+","B","B-","C+","C","C-","D"}
FAILING_GRADES = {"F"}
EXCLUDE_GRADES = {"IP","W", None}


def grade_analytics(request):
    courses = Course.objects.all().order_by("code")

    labels = []
    pass_counts = []
    fail_counts = []
    avg_marks = []

    for c in courses:
        qs = c.enrollments.all()
        passes = qs.filter(grade__in=PASSING_GRADES).count()
        fails = qs.filter(grade__in=FAILING_GRADES).count()
        labels.append(c.code)
        pass_counts.append(passes)
        fail_counts.append(fails)
        avg_marks.append(qs.exclude(marks__isnull=True).aggregate(Avg("marks"))["marks__avg"] or 0)

    # Overall grade distribution
    grade_dist = (
        Enrollment.objects
        .exclude(grade__isnull=True)
        .values("grade")
        .annotate(total=Count("id"))
        .order_by("grade")
    )
    grade_labels = [g["grade"] for g in grade_dist]
    grade_values = [g["total"] for g in grade_dist]

    context = {
        "labels": labels,
        "pass_counts": pass_counts,
        "fail_counts": fail_counts,
        "avg_marks": avg_marks,
        "grade_labels": grade_labels,
        "grade_values": grade_values,
    }
    return render(request, "analytics/grade_analytics.html", context)


def student_dashboard(request, student_id: int):
    student = get_object_or_404(Student, pk=student_id)
    enrollments = student.enrollments.select_related("course").order_by("-enrolled_on")

    course_labels = [e.course.code for e in enrollments]
    marks_values = [(e.marks or 0) for e in enrollments]

    # GPA (simple 4.0 scale mapping)
    grade_points = {
        "A+": 4.0, "A": 4.0, "A-": 3.7,
        "B+": 3.3, "B": 3.0, "B-": 2.7,
        "C+": 2.3, "C": 2.0, "C-": 1.7,
        "D": 1.0, "F": 0.0,
    }
    total_points = 0.0
    total_credits = 0
    for e in enrollments:
        gp = grade_points.get(e.grade)
        if gp is not None:
            total_points += gp * e.course.credits
            total_credits += e.course.credits
    gpa = round(total_points / total_credits, 2) if total_credits else None

    context = {
        "student": student,
        "enrollments": enrollments,
        "course_labels": course_labels,
        "marks_values": marks_values,
        "gpa": gpa,
    }
    return render(request, "analytics/student_dashboard.html", context)


def department_reports(request):
    # Aggregate by department
    courses = Course.objects.all()
    data = []
    for dept_value, dept_label in Course.DEPARTMENT_CHOICES:
        dept_courses = courses.filter(department=dept_value)
        enrollments = Enrollment.objects.filter(course__in=dept_courses)
        total_enrolled = enrollments.count()
        avg_marks = enrollments.exclude(marks__isnull=True).aggregate(Avg("marks"))["marks__avg"] or 0
        pass_count = enrollments.filter(grade__in=PASSING_GRADES).count()
        fail_count = enrollments.filter(grade__in=FAILING_GRADES).count()
        pass_rate = round((pass_count / (pass_count + fail_count) * 100), 2) if (pass_count + fail_count) else 0
        data.append({
            "code": dept_value,
            "label": dept_label,
            "total_courses": dept_courses.count(),
            "total_enrolled": total_enrolled,
            "avg_marks": round(avg_marks, 2) if avg_marks else 0,
            "pass_rate": pass_rate,
        })

    context = {
        "departments": data,
        "dept_labels": [row["label"] for row in data],
        "dept_enrollments": [row["total_enrolled"] for row in data],
        "dept_pass_rates": [row["pass_rate"] for row in data],
        "dept_avg_marks": [row["avg_marks"] for row in data],
    }
    return render(request, "analytics/department_reports.html", context)
