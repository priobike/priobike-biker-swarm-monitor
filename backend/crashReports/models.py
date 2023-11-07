from django.contrib.gis.db import models
from django.utils import timezone

class CrashReport(models.Model):
    """A Crash report."""

    # The time since the start of the biker simulation.
    startTime = models.DateTimeField(default=timezone.now)

    # The time since the start of the biker simulation.
    crashTime = models.DateTimeField(default=timezone.now)

    # The error message that got displayed
    errorMsg = models.TextField(default="")

    # The name of the service that crashed.
    serviceName = models.CharField(max_length=255)

    def __str__(self) -> str:
        return f"Biker started {self.startTime}, crashed {self.crashTime} at Service {self.serviceName} with: {self.errorMsg}"

    class Meta:
        verbose_name = "CrashReport"
        verbose_name_plural = "CrashReports"

