from django.urls import path, re_path, include
from django.contrib.auth import views

from django.contrib.auth.views import LoginView

from .views import HomeView, PatientFileView
from .views.patient_file import NewPatientView, PatientListView, SettingsView

app_name = "core"

root_urlpatterns = [
    path("", HomeView.as_view(), name="home"),
    path("settings/", SettingsView.as_view(), name="settings"),
    path("patient/", PatientListView.as_view(), name="patient_list"),
    path("patient/file/<pk>", PatientFileView.as_view(), name="patient_file"),
    path("patient/add/", NewPatientView.as_view(), name="patient_new"),
    path("accounts/", include("django.contrib.auth.urls")),
]

# Django login accounts views:
# accounts/login/ [name='login']
# accounts/logout/ [name='logout']
# accounts/password_change/ [name='password_change']
# accounts/password_change/done/ [name='password_change_done']
# accounts/password_reset/ [name='password_reset']
# accounts/password_reset/done/ [name='password_reset_done']
# accounts/reset/<uidb64>/<token>/ [name='password_reset_confirm']
# accounts/reset/done/ [name='password_reset_complete']
