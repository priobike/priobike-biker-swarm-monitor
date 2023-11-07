from django.urls import path

from . import views

app_name = 'crashReports'

urlpatterns = [
    path("crash/post/", views.PostCrashReportResource.as_view(), name="send-crash-report"),
    path("success/post/", views.PostSuccessReportResource.as_view(), name="send-success-report"),
    path("metrics", views.GetMetricsResource.as_view(), name="get-metrics")
]
