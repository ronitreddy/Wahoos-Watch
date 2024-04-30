"""
URL configuration for mysite project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
import debug_toolbar
from django.contrib import admin
from django.contrib.auth.views import LogoutView
from django.urls import path, include, reverse_lazy
from django.contrib.auth import views as auth_views
from django.views.generic import RedirectView
from nbhood_watch import views
from nbhood_watch.views import login_views

from nbhood_watch.views.login_views import login

urlpatterns = [
    #path('', RedirectView.as_view(url = 'nbhood_watch/login', permanent=False)),
    path('nbhood_watch/', include('nbhood_watch.urls')),
    path('admin/', admin.site.urls),
    path('', RedirectView.as_view(pattern_name='nbhood_watch:login', permanent=False), name='root'),
    path('logout/',LogoutView.as_view(), name='logout'),
    path('social-auth/', include('social_django.urls', namespace='social')),
    path('home/', login_views.home, name='home'),
    path('__debug__/', include(debug_toolbar.urls)),
]