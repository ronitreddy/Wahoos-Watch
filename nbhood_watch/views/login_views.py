from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.views.generic import TemplateView

from mysite import settings
from nbhood_watch.models import Submission


def login(request):
    if request.user.is_authenticated:
        logout(request)
    submissions = Submission.objects.filter(latitude__isnull=False, longitude__isnull=False, submission_visibility="Public", submission_verification="Verified")
    alerts = Submission.objects.filter(submission_visibility="Public", submission_verification="Verified").order_by('-submission_date')
    context = {
        'google_maps_api_key': settings.GOOGLE_MAPS_API_KEY,
        'submissions': submissions,
        'alerts': alerts
    }
    return render(request, 'nbhood_watch/login.html', context)


def isSiteAdmin(user):
    django_admin = user.is_superuser and user.is_staff
    if user.has_perm('nbhood_watch.view_submission') and not django_admin:
        return True


def isCommonUser(user):
    return not isSiteAdmin(user)


def admin_required(view_func):
    def wrapper(request, *args, **kwargs):
        if request.user.is_authenticated and isSiteAdmin(request.user):
            return view_func(request, *args, **kwargs)
        else:
            return redirect('nbhood_watch:access_denied')
    return wrapper


def common_user_required(view_func):
    def wrapper(request, *args, **kwargs):
        if request.user.is_authenticated and isCommonUser(request.user):
            return view_func(request, *args, **kwargs)
        else:
            return redirect('nbhood_watch:access_denied')
    return wrapper


@login_required
def home(request):
    if request.user.is_authenticated:
        user = request.user
        first_name = user.first_name
        last_name = user.last_name
        email = user.email
        if not User.objects.filter(email=email).exists():
            User.objects.create(first_name=first_name, last_name=last_name, email=email)

        if isSiteAdmin(user):
            return redirect('nbhood_watch:admin_info')
        return redirect('nbhood_watch:user_info')


@common_user_required
def user_info(request):
    return render(request, 'nbhood_watch/user_info.html')


@admin_required
def admin_info(request):
    return render(request, 'nbhood_watch/admin_info.html')


def access_denied(request):
    return render(request, 'nbhood_watch/access_denied.html')


def anonymous_info(request):
    return render(request, 'nbhood_watch/anonymous_info.html')


class LogOutView(TemplateView):
    template_name = "nbhood_watch/logged_out.html"
