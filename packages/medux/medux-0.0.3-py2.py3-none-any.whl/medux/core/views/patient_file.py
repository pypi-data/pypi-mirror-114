from django.views.generic import DetailView, CreateView, ListView, TemplateView

from medux.core.models import Patient
from medux.core.views import MeduxBaseMixin


class PatientListView(MeduxBaseMixin, ListView):
    model = Patient
    permission_required = "can list patients"
    context_object_name = "patient_list"


class PatientFileView(MeduxBaseMixin, DetailView):
    # template_name = "patient_detail.html"
    permission_required = "can view patients"
    model = Patient

    # def get_context_data(self, *args, **kwargs):
    #     context = super().get_context_data(*args, **kwargs)
    #     return context


class NewPatientView(MeduxBaseMixin, CreateView):
    model = Patient
    permission_required = "can add patients"
    fields = ["names"]


class SettingsView(MeduxBaseMixin, TemplateView):
    template_name = "core/settings.html"
    permission_required = "core.canadmin"
