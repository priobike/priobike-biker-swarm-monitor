import json

from django.conf import settings
from crashReports.models import CrashReport, SuccessReport
from django.db.models import Count
from django.http import HttpResponseBadRequest, JsonResponse, HttpResponseServerError, HttpResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import View
from datetime import datetime

@method_decorator(csrf_exempt, name='dispatch')
class PostCrashReportResource(View):
    def post(self, request):
        try:
            json_data = json.loads(request.body)
        except json.JSONDecodeError:
            return HttpResponseBadRequest(json.dumps({"error": "Invalid request."}))
        
        try:
            CrashReport.objects.create(
                startTime=datetime.fromtimestamp(json_data['startTime']),
                crashTime=datetime.fromtimestamp(json_data['crashTime']),
                errorMsg=json_data['errorMsg'],
                serviceName=json_data['serviceName']
            )
        except (KeyError):
            return HttpResponseBadRequest(json.dumps({"error": "Invalid request."}))
        except Exception as e:
            return HttpResponseServerError(json.dumps({"error": "Internal server error."}))

        return JsonResponse({"success": True})
    
@method_decorator(csrf_exempt, name='dispatch')
class PostSuccessReportResource(View):
    def post(self, request):
        try:
            json_data = json.loads(request.body)
        except json.JSONDecodeError:
            return HttpResponseBadRequest(json.dumps({"error": "Invalid request."}))
        
        try:
            SuccessReport.objects.create(
                startTime=datetime.fromtimestamp(json_data['startTime']),
                endTime=datetime.fromtimestamp(json_data['endTime']),
            )
        except (KeyError):
            return HttpResponseBadRequest(json.dumps({"error": "Invalid request."}))
        except Exception as e:
            return HttpResponseServerError(json.dumps({"error": "Internal server error."}))

        return JsonResponse({"success": True})
    

@method_decorator(csrf_exempt, name='dispatch')
class GetMetricsResource(View):
    def get(self, request):
        """
        Generate Prometheus metrics as a text file and return it.
        """
        # Only allow access with a valid api key.
        api_key = request.GET.get("api_key", None)
        if not api_key or api_key != settings.API_KEY:
            return HttpResponseBadRequest()

        metrics = []

        # Count number of total successful biker runs.
        metrics.append(f'n_success_reports {SuccessReport.objects.count()}')

        # Count the number of crash reports for each error message and service name.
        counts = CrashReport.objects \
            .values("errorMsg", "serviceName") \
            .annotate(v=Count('errorMsg')) \
            .values_list("errorMsg", "serviceName", "v")
        for errorMsg, serviceName, count in counts:
            metrics.append(f'n_crash_reports{{service_name="{serviceName}", error_msg="{errorMsg}"}} {count}')
        
        # Average times TODO.

        content = '\n'.join(metrics) + '\n'
        return HttpResponse(content, content_type='text/plain')

