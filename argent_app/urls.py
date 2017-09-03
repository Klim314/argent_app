"""coresite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from django.contrib.auth.decorators import login_required
from argent_app import views

urlpatterns = [
    url(r'^$', views.Index.as_view(), name="index"),
    url(r'^manage/', login_required(views.Manage.as_view()), name='room_manage'),
    url(r'^join/', views.Join.as_view(), name='room_join'),
    url(r'^create/', login_required(views.Create.as_view()), name='room_create'),
    url(r'^browse/', login_required(views.Browse.as_view()), name='room_browse'),
    url(r'^join/', login_required(views.View.as_view()), name='room_join'),
]
