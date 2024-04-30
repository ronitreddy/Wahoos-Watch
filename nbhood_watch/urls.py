from django.contrib.auth.views import LogoutView
from django.urls import path

from nbhood_watch import views
from nbhood_watch.views.login_views import *
from nbhood_watch.views.report_views import *
from nbhood_watch.views.views import *

app_name = 'nbhood_watch'
urlpatterns = [
    path('', IndexView.as_view(), name="index"),
    path('login/', login, name='login'),
    path("logout/", LogoutView.as_view(), name="logout"),
    path('access-denied/', access_denied, name='access_denied'),
    path('user-info/', user_info, name='user_info'),
    path('admin-info/', admin_info, name='admin_info'),
    path('anonymous-info/', anonymous_info, name='anonymous_info'),
    path('anonymous-report/', anonymous_report, name='anonymous_report'),
    path('user-report/', user_report, name='user_report'),
    path('view_reports/', view_reports, name='view_reports'),
    path('update_submission_status/', update_submission_status, name='update_submission_status'),
    path('user-submit/', user_submit, name='user_submit'),
    path('anonymous-submit', anonymous_submit, name='anonymous_submit'),
    path('user-history/', user_history, name='user_history'),
    path('user-history-submission-info/<int:submission_id>', user_history_submission_info, name='user_history_submission_info'),
    path('alert-info/<int:submission_id>', alert_info, name='alert_info'),
    path('delete-submission/<int:submission_id>/', delete_submission, name='delete_submission'),
    path('submission-info/<int:submission_id>/', submission_info, name='submission_info'),
    path('emergency_contact/', emergency_contact, name='emergency_contact'),
    path('update-submission-status-on-view-details/', update_submission_status_on_view_details, name='update_submission_status_on_view_details'),
]