from django.urls import path

from . import views

app_name = 'crashReports'

urlpatterns = [
    path("post/", views.PostCrashReportResource.as_view(), name="send-crash-report"),
    path("get/", views.GetCrashReport.as_view(), name="receive-crash-reports"),
]
