from django.contrib import admin

from .models import *

@admin.register(Submission)
class SubmissionAdmin(admin.ModelAdmin):
    list_display = ('submission_date',)
    ordering = ('-submission_date',)

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('last_name', 'first_name')
