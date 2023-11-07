from django.contrib.gis.db import models
from django.utils import timezone

class CrashReport(models.Model):
    """A Crash Report."""

    # The time since the start of the biker simulation.
    startTime = models.DateTimeField(default=timezone.now)

    # The time when the crash of the biker simulation occured.
    crashTime = models.DateTimeField(default=timezone.now)

    # The error message that got displayed.
    errorMsg = models.TextField(default="")

    # The name of the service that crashed.
    serviceName = models.CharField(max_length=255)

    def __str__(self) -> str:
        return f"Biker started {self.startTime}, crashed {self.crashTime} at Service {self.serviceName} with: {self.errorMsg}"

    class Meta:
        verbose_name = "CrashReport"
        verbose_name_plural = "CrashReports"

class SuccessReport(models.Model):
    """A Success Report"""

    # The time since the start of the biker simulation.
    startTime = models.DateTimeField(default=timezone.now)

    # The time when the biker simulation finished successfully.
    endTime = models.DateTimeField(default=timezone.now)

    def __str__(self) -> str:
        return f"Biker started {self.startTime} and finished {self.endTime}"

    class Meta:
        verbose_name = "SuccessReport"
        verbose_name_plural = "SuccessReports"
