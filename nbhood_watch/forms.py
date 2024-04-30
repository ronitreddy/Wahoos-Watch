from django import forms
from .models import *
from django.core.exceptions import ValidationError
from multiupload.fields import MultiFileField, MultiMediaField, MultiImageField


class ReportForm(forms.ModelForm):
    class Meta:
        model = Submission
        exclude = ['submission_user', 'submission_date', 'submission_file', 'submission_response']
        widgets = {
            'latitude': forms.HiddenInput(),
            'longitude': forms.HiddenInput(),
        }

    submission_files = MultiFileField(min_num=1, max_num=10, max_file_size=1024 * 1024 * 5, required=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['submission_verification'].widget = forms.HiddenInput()
        self.fields['submission_admin_notes'].widget = forms.HiddenInput()
        self.fields['submission_title'].widget.attrs.update({'style': 'max-height: 70px;'})
    #     self.fields['submission_file'].widget.attrs.update({'multiple': True})

    def save(self, commit=True):
        submission = super().save(commit=False)
        submission.save()
        files = self.cleaned_data.get('submission_files')
        if files:
            for file in files:
                SubmissionFile.objects.create(submission=submission, file=file)

        return submission

    def clean(self):
        cleaned_data = super().clean()
        submission_description = cleaned_data.get('submission_description')
        submission_files = cleaned_data.get('submission_file')
        submission_title = cleaned_data.get('submission_title')

        if not submission_title:
            self.add_error('submission_title', "Submission title is required.")
        if not submission_description:
            self.add_error('submission_description', "Submission description is required.")

        return cleaned_data

    def clean_submission_status(self):
        status = self.cleaned_data.get('submission_status')
        if status != 'New':
            raise ValidationError("Status must be 'New'")
        return status


class UpdateStatusForm(forms.ModelForm):
    class Meta:
        model = Submission
        fields = ['submission_status']
