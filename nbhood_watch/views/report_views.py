from mysite import settings
from nbhood_watch.models import User, Submission, SubmissionFile
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from nbhood_watch.forms import ReportForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.files.storage import default_storage

from nbhood_watch.views import login_views


def anonymous_report(request):
    if request.method == 'POST':
        form = ReportForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('nbhood_watch:anonymous_submit'))
    else:
        form = ReportForm()
    return render(request, 'nbhood_watch/anonymous_report.html',
                  {"form": form, 'google_maps_api_key': settings.GOOGLE_MAPS_API_KEY})


def user_report(request):
    if request.method == 'POST':
        form = ReportForm(request.POST, request.FILES)
        if form.is_valid():
            submission = form.save(commit=True)
            first_name = request.user.first_name
            last_name = request.user.last_name
            email = request.user.email
            user = User.objects.get_or_create(
                first_name=first_name,
                last_name=last_name,
                email=email
            )[0]
            submission.submission_user = user
            submission.save()

            return HttpResponseRedirect(reverse('nbhood_watch:user_submit'))
    else:
        form = ReportForm()
    return render(request, 'nbhood_watch/user_report.html',
                  {"form": form, "google_maps_api_key": settings.GOOGLE_MAPS_API_KEY})


def view_reports(request):
    submissions = Submission.objects.order_by('-submission_date').all()
    return render(request, 'nbhood_watch/view_reports.html', {'submissions': submissions})


def update_submission_status(request):
    if request.method == 'POST':
        submission_id = request.POST.get('submission_id')
        new_status = request.POST.get('status')
        submission = get_object_or_404(Submission, id=submission_id)
        submission.submission_status = new_status
        submission.save()
        return redirect('nbhood_watch:view_reports')
    return redirect('nbhood_watch:view_reports')


def update_submission_status_on_view_details(request):
    if request.method == 'POST':
        submission_id = request.POST.get('submission_id')
        new_status = request.POST.get('status')
        new_verification = request.POST.get('verification')
        admin_notes = request.POST.get('admin_notes')
        submission = get_object_or_404(Submission, id=submission_id)
        submission.submission_status = new_status
        submission.submission_verification = new_verification
        submission.submission_admin_notes = admin_notes
        submission.save()
        return redirect('nbhood_watch:submission_info', submission_id=submission_id)
    return redirect('nbhood_watch:view_reports')


def anonymous_submit(request):
    return render(request, 'nbhood_watch/anonymous_submit.html')


def user_submit(request):
    return render(request, 'nbhood_watch/user_submit.html')


@login_required
def user_history(request):
    if request.user.is_authenticated:
        submissions = Submission.objects.filter(submission_user__email=request.user.email)
        return render(request, 'nbhood_watch/user_history.html', {'submissions': submissions})
    else:
        return redirect('nbhood_watch:login')


@login_required
def delete_submission(request, submission_id):
    submission = get_object_or_404(Submission, pk=submission_id)

    for submission_file in SubmissionFile.objects.filter(submission=submission):
        file_path = submission_file.file.name
        default_storage.delete(file_path)

    submission.delete()

    messages.success(request, 'Submission deleted successfully.')
    return HttpResponseRedirect(reverse('nbhood_watch:user_history'))


@login_required
def submission_info(request, submission_id):
    submission = get_object_or_404(Submission, pk=submission_id)
    is_admin = login_views.isSiteAdmin(request.user)
    return render(request, 'nbhood_watch/submission_info.html',
                  {'submission': submission, 'is_admin': is_admin, 'google_maps_api_key': settings.GOOGLE_MAPS_API_KEY})


@login_required
def user_history_submission_info(request, submission_id):
    submission = get_object_or_404(Submission, pk=submission_id)
    is_admin = login_views.isSiteAdmin(request.user)
    return render(request, 'nbhood_watch/user_history_submission_info.html',
                  {'submission': submission, 'is_admin': not is_admin,
                   'google_maps_api_key': settings.GOOGLE_MAPS_API_KEY})


def alert_info(request, submission_id):
    submission = get_object_or_404(Submission, pk=submission_id)
    is_admin = login_views.isSiteAdmin(request.user)
    return render(request, 'nbhood_watch/alert_info.html',
                  {'submission': submission, 'is_admin': not is_admin,
                   'google_maps_api_key': settings.GOOGLE_MAPS_API_KEY})


def emergency_contact(request):
    return render(request, 'nbhood_watch/emergency_contact.html')
