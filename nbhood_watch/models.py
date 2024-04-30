from django.db import models
from django.contrib import admin
import uuid


def submission_file_path(instance, filename):
    unique_filename = f"{uuid.uuid4()}_{filename}"
    return f'uploads/{unique_filename}'


class Submission(models.Model):
    # add short description
    submission_user = models.ForeignKey(verbose_name='Submission User', to='User',
                                        on_delete=models.CASCADE, null=True, blank=True)
    submission_date = models.DateTimeField("Report Date:", auto_now_add=True)
    submission_title = models.TextField(max_length=300, null=True, blank=True, help_text="*required")
    submission_description = models.TextField(max_length=1000, null=True, blank=True, help_text="*required")
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)
    submission_file = models.FileField(upload_to=submission_file_path, null=True, blank=True)

    # Need to manually update time if submission is updated

    # Add choices for report status
    STATUS_CHOICES = [
        ('New', 'New'),
        ('In Progress', 'In Progress'),
        ('Reviewed', 'Reviewed'),
    ]
    submission_status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='New')
    submission_response = models.TextField(null=True, blank=True)

    CATEGORY_CHOICES = [
        ('Safety Concerns', 'Safety Concerns'),
        ('Environmental Issues', 'Environmental Issues'),
        ('Public Disturbances', 'Public Disturbances'),
        ('Illegal Activities', 'Illegal Activities'),
        ('Maintenance Issues', 'Maintenance Issues'),
        ('Lost/Found Items', 'Lost/Found Items'),
        ('Other', 'Other'),
    ]
    submission_category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='Safety Concerns')

    VISIBILITY_CHOICES = [
        ('Public', 'Public'),
        ('Only to Admin', 'Only to Admin'),
    ]
    submission_visibility = models.CharField(max_length=20, choices=VISIBILITY_CHOICES, default='Public')

    VERIFICATION_CHOICES = [
        ('Verified', 'Verified'),
        ('Unverified', 'Unverified'),
        ('False Information', 'False Information'),
    ]
    submission_verification = models.CharField(max_length=20, choices=VERIFICATION_CHOICES, default='Unverified')
    submission_admin_notes = models.TextField(null=True, blank=True, default='N/A')
    def __str__(self):
        return f"User: {self.submission_user},\n Date: {self.submission_date.strftime('%Y-%m-%d %H:%M:%S')}\n"


class SubmissionFile(models.Model):
    # Add code to connect to user so we can get the email of the user submitting the files
    submission = models.ForeignKey(Submission, on_delete=models.CASCADE, related_name='files')
    file = models.FileField(upload_to=submission_file_path)

    def __str__(self):
        return f"File: {self.file.name}"


class User(models.Model):
    first_name = models.CharField(max_length=100, null=True, blank=True, default='Anon')
    last_name = models.CharField(max_length=100, null=True, blank=True, default='Anon')
    email = models.EmailField(null=False, blank=False, default="<ANON@gmail.com>")
    last_login = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.email} {self.first_name} {self.last_name}"
