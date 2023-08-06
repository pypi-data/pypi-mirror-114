from django.urls import path
from . import views

# namespaced URLs
app_name = "medux_prescriptions"

# URLs namespaced  under medux_prescriptions/
urlpatterns = [
    # path("", views.IndexView.as_view(), name="index"),
]


# global URLs
root_urlpatterns = [
    # path("api/foo", views.APIView.as_view(), name="api"),
]
