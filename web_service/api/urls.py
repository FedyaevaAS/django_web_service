from django.urls import path

from .views import FileUploadView, TopClientsView

urlpatterns = [
    path("upload/", FileUploadView.as_view(), name="csv_upload"),
    path("top-clients/", TopClientsView.as_view(), name="top-clients-list"),
]
