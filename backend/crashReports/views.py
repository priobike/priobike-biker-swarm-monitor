import json

from crashReports.models import CrashReport
from django.http import HttpResponseBadRequest, JsonResponse, HttpResponseServerError
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import View

@method_decorator(csrf_exempt, name='dispatch')
class PostCrashReportResource(View):
    def post(self, request):
        try:
            json_data = json.loads(request.body)
        except json.JSONDecodeError:
            return HttpResponseBadRequest(json.dumps({"error": "Invalid request."}))
        
        try:
            CrashReport.objects.create(
                timeSinceStart=json_data['timeSinceStart'],
                errorMsg=json_data['errorMsg'],
            )
        except (KeyError):
            return HttpResponseBadRequest(json.dumps({"error": "Invalid request."}))
        except Exception as e:
            return HttpResponseServerError(json.dumps({"error": "Internal server error."}))

        return JsonResponse({"success": True})
    

@method_decorator(csrf_exempt, name='dispatch')
class GetCrashReport(View):
    def get(self, request):
        print(CrashReport.objects.all())

        return JsonResponse({"success": CrashReport.objects.all()})
        
