import os
import django
from django.core.files.uploadedfile import SimpleUploadedFile
from django.contrib.auth import get_user_model

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mysite.settings")
django.setup()

from .models import *
from django.utils import timezone
from nbhood_watch.models import User
from django.urls import reverse
from django.test import TestCase, Client
from nbhood_watch.models import Submission
from django.contrib.auth.hashers import make_password


class testUser(TestCase):
    def test_user_creation(self):
        user = User.objects.create(first_name='John', last_name='Smith', email="JohnSmith@gmail.com")
        saved_user = User.objects.get(email="JohnSmith@gmail.com")

        self.assertEqual(saved_user.first_name, "John")
        self.assertEqual(saved_user.last_name, "Smith")
        self.assertEqual(saved_user.email, "JohnSmith@gmail.com")


class SubmissionModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create(first_name='Mary', last_name='Doe', email="MaryDoe@gmail.com")

    def test_submission_creation(self):
        submission = Submission.objects.create(submission_user=self.user)
        submission.save()  # Explicit save, to ensure it's committed

        saved_submission = Submission.objects.order_by('pk').last()

        self.assertIsNotNone(saved_submission, "The saved_submission object is None")

        self.assertEqual(saved_submission.submission_user, self.user,
                         f"Submission user ID does not match: {saved_submission.submission_user_id} vs {self.user.id}")


class AnonymousReportViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.url = reverse('nbhood_watch:anonymous_report')

    def test_get_anonymous_report(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'nbhood_watch/anonymous_report.html')

    def test_post_anonymous_report(self):
        initial_count = Submission.objects.count()

        response = self.client.post(self.url, {
            'submission_title':'Test Submission',
            'submission_description': 'Test Report',
            "submission_status": "New",
            "submission_category": "Lost/Found Items",
            'submission_files': [],
            "submission_visibility": "Public",
            "submission_verification": "Verified",
            "submission_admin_notes": "None",

        })
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Submission.objects.count(), initial_count + 1)

        new_submission = Submission.objects.latest('id')
        self.assertIsNone(new_submission.submission_user)

    def test_post_anonymous_report_with_file(self):
        initial_count = Submission.objects.count()
        dummy_file = SimpleUploadedFile('test_file.png', b'This is a test file')

        response = self.client.post(self.url, {
            'submission_title': 'Test Submission',
            'submission_description': 'Test Report',
            "submission_status": "New",
            "submission_category": "Public Disturbances",
            'submission_files': [dummy_file],
            "submission_visibility": "Public",
            "submission_verification": "Verified",
            "submission_admin_notes": "None",
        })

        self.assertEqual(response.status_code, 302)
        self.assertEqual(Submission.objects.count(), initial_count + 1)
        new_submission = Submission.objects.latest('id')
        self.assertIsNotNone(new_submission.submission_file)
        self.assertIsNone(new_submission.submission_user)

    def test_post_anonymous_report_with_multiplefile(self):
        initial_count = Submission.objects.count()
        dummy_file = SimpleUploadedFile('test_file.png', b'This is a test file')
        file_test = SimpleUploadedFile('test_file.pdf', b'This is a test file')

        response = self.client.post(self.url, {
            'submission_title': 'Test Submission',
            'submission_description': 'Test Report',
            "submission_status": "New",
            "submission_category": "Maintenance Issues",
            'submission_files': [dummy_file, file_test],
            "submission_visibility": "Public",
            "submission_verification": "Verified",
            "submission_admin_notes": "None",
        })

        self.assertEqual(response.status_code, 302)
        self.assertEqual(Submission.objects.count(), initial_count + 1)
        new_submission = Submission.objects.latest('id')
        self.assertIsNotNone(new_submission.submission_file)
        self.assertIsNone(new_submission.submission_user)


class SubmissionTestCase(TestCase):
    def setUp(self):
        User = get_user_model()
        self.user = User.objects.create_user(
            username='testuser',
            first_name='John',
            last_name='Doe',
            email='john.doe@example.com',
            password='testpassword123'
        )

    def test_user_submission(self):
        # Log in the test user
        self.client.login(username='testuser', password='testpassword123')

        dummy_file = SimpleUploadedFile('dummy_file.pdf', b'These are the contents of the dummy file.')

        post_data = {
            'submission_title': 'Test Submission',
            'submission_description': 'Test Report Description',
            'submission_status': 'New',
            "submission_category": "Lost/Found Items",
            'submission_files': [dummy_file],
            "submission_visibility": "Public",
            "submission_verification": "Verified",
            "submission_admin_notes": "None",
        }

        response = self.client.post(reverse('nbhood_watch:user_report'), post_data)

        self.assertRedirects(response, reverse('nbhood_watch:user_submit'), msg_prefix="Redirect failed")

        submission = Submission.objects.latest('id')
        self.assertEqual(submission.submission_user.email, self.user.email, "Submission user does not match")
