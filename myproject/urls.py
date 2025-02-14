"""myproject URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
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
from django.contrib import admin
from django.urls import path, re_path
from app import views as main_views
import django.contrib.auth.views
from django.contrib.auth.views import LoginView, LogoutView
from datetime import datetime
from app import views
from app.views import medical_cat_detail, create_treatment

admin.autodiscover()

urlpatterns = [
    path('admin/', admin.site.urls),
    re_path(r'^$', main_views.home, name='home'),
    re_path(r'^contact$', main_views.contact, name='contact'),
    re_path(r'^about$', main_views.about, name='about'),
    re_path(r'^login/$',
        LoginView.as_view(template_name = 'app/login.html'),
        name='login'),
    re_path(r'^logout$',
        LogoutView.as_view(template_name = 'app/index.html'),
        name='logout'),
    re_path(r'^menu$', main_views.menu, name='menu'),
    path('create-account/', views.create_account, name='create_account'),
    path('configure-account/', views.configure_account, name='configure_account'),
    path('change-password/', views.change_password, name='change_password'),
    path('system_settings', views.system_settings, name='system_settings' ),
    path('cat-list/', views.cat_list, name='cat_list'),
    path('create-cat/', views.create_cat, name='create_cat'),
    path('cat-details/<int:cat_id>/', views.cat_details, name='cat_details'),
    path('cat-scheduler-checkup/<int:cat_id>/', views.cat_scheduler_checkup, name='cat_scheduler_checkup'),

    path('medical_cat_detail/<int:cat_id>/', medical_cat_detail, name='medical_cat_detail'),
    path('medical-cat-list/', views.medical_cat_list, name='medical_cat_list'),
    path('caretaker-duty-panel/', views.caretaker_duty_panel, name='caretaker_duty_panel'),
    path('create-treatment/<int:cat_id>/', views.create_treatment, name='create_treatment'),
    path("backup_database/", views.backup_database, name="backup_database"),
    path("import_database/", views.import_database, name="import_database"),
    path('report/', views.report, name='report'),




]
