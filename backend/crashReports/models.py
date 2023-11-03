from django.contrib.gis.db import models

class CrashReport(models.Model):
    """A Crash report."""

    # The time since the start of the biker simulation.
    timeSinceStart = models.FloatField(default=0)

    # The error message that got displayed
    errorMsg = models.TextField(default="")

    def __str__(self) -> str:
        return f"Ran {self.timeSinceStart} and exited with: {self.errorMsg} at {self.timeSinceStart}"

    class Meta:
        verbose_name = "CrashReport"
        verbose_name_plural = "CrashReports"

