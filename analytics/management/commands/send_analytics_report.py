from django.core.management.base import BaseCommand, CommandError
from django.core.mail import send_mail
from django.conf import settings
from django.template.loader import render_to_string
from django.db.models import Avg, Count
from enrollments.models import Enrollment
from courses.models import Course

PASSING = {"A+","A","A-","B+","B","B-","C+","C","C-","D"}
FAILING = {"F"}

class Command(BaseCommand):
    help = "Send analytics report via email. Usage: manage.py send_analytics_report --email you@example.com --frequency weekly|monthly"

    def add_arguments(self, parser):
        parser.add_argument("--email", required=True, help="Recipient email")
        parser.add_argument("--frequency", choices=["weekly", "monthly"], default="weekly")

    def handle(self, *args, **opts):
        to_email = opts["email"]
        freq = opts["frequency"]

        top_courses = (
            Course.objects
            .annotate(enrolled=Count("enrollments"))
            .order_by("-enrolled")[:5]
        )
        avg_marks = Enrollment.objects.exclude(marks__isnull=True).aggregate(Avg("marks"))["marks__avg"]
        pass_count = Enrollment.objects.filter(grade__in=PASSING).count()
        fail_count = Enrollment.objects.filter(grade__in=FAILING).count()
        total_graded = pass_count + fail_count
        pass_rate = round(pass_count/total_graded*100, 2) if total_graded else 0

        context = {
            "frequency": freq.title(),
            "top_courses": top_courses,
            "avg_marks": round(avg_marks, 2) if avg_marks else None,
            "pass_rate": pass_rate,
            "total_enrollments": Enrollment.objects.count(),
        }

        subject = f"Student Management Analytics Report ({freq.title()})"
        message = render_to_string("analytics/email_report.txt", context)

        try:
            send_mail(subject, message, getattr(settings, "DEFAULT_FROM_EMAIL", None), [to_email])
            self.stdout.write(self.style.SUCCESS(f"Analytics report sent to {to_email}"))
        except Exception as exc:
            # Fallback: print report to stdout if email fails
            self.stdout.write(self.style.WARNING("Email sending failed; printing report to console."))
            self.stdout.write(message)
            self.stdout.write(self.style.ERROR(str(exc)))
