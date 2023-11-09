import json

import math
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
        
        countsSanitized = []
        # Sanitize error messages.
        for errorMsg, serviceName, count in counts:
            countsSanitized.append({"serviceName": serviceName, "errorMsg": getSanitizedMessage(errorMsg), "count": count})

        # Fix counters.
        countsSanitizedFixed = []
        for countSanitized in countsSanitized:
        
            isNew = True
            for countSanitizedFixed in countsSanitizedFixed:
                if countSanitizedFixed["serviceName"] == countSanitized["serviceName"] and countSanitizedFixed["errorMsg"] == countSanitized["errorMsg"]:
                    isNew = False
                    countSanitizedFixed["count"] += 1
            
            if isNew:
                countsSanitizedFixed.append(countSanitized)

        
        for countSanitizedFixed in countsSanitizedFixed:
            metrics.append(f'n_crash_reports{{service_name="{countSanitizedFixed["serviceName"]}", error_msg="{countSanitizedFixed["errorMsg"]}"}} {countSanitizedFixed["count"]}')
        

            
        
        
        # Count the number of durations in time intervalls of 10 seconds for success reports.
        binSize = 10 # Size in seconds.
        
        durations = []
        maxDuration = 0 # Max duration of a report.
        

        successReports = SuccessReport.objects \
            .values_list("startTime", "endTime") 
        
        # Get all durations.
        for startTime, endTime in successReports:
            duration = endTime - startTime
            if duration.total_seconds() >= 0 and duration.total_seconds() < 60 * 60:
                durations.append(duration.total_seconds())

        bins = {}
        # Create bins for durations and count them.
        for duration in durations:
            # Cast duration to bin range.
            ratio = math.trunc(duration / binSize)
            binRangeName = getBinRangeNameByDuration(ratio, binSize)

            # Add duration to bins.
            if binRangeName in bins:
                bins[binRangeName] += 1
            else:
                # Add new bins to bins.
                for i in range(maxDuration, ratio + 1):
                    binName = getBinRangeNameByDuration(i, binSize)
                    bins[binName] = 0
                maxDuration = ratio + 1
                bins[getBinRangeNameByDuration(math.trunc(duration / binSize), binSize)] += 1

        for key, value in bins.items():
            metrics.append(f'n_success_durations{{bin="{key}"}} {value}')

        # Count the number of duration in time intervalls of 10 seconds for crash reports.
        durations = []
        maxDuration = 0

        crashReports = CrashReport.objects \
            .values_list("startTime", "crashTime") 
        
        # Get all durations.
        for startTime, crashTime in crashReports:
            duration = crashTime - startTime
            if duration.total_seconds() >= 0 and duration.total_seconds() < 60 * 60:
                durations.append(duration.total_seconds())
        
        bins = {}
        # Create bins for durations and count them.
        for duration in durations:
            # Cast duration to bin range.
            ratio = math.trunc(duration / binSize)
            binRangeName = getBinRangeNameByDuration(ratio, binSize)

            # Add duration to bins.
            if binRangeName in bins:
                bins[binRangeName] += 1
            else:
                # Add new bins to bins.
                for i in range(maxDuration, ratio + 1):
                    binName = getBinRangeNameByDuration(i, binSize)
                    bins[binName] = 0
                maxDuration = ratio + 1
                bins[getBinRangeNameByDuration(math.trunc(duration / binSize), binSize)] += 1

        for key, value in bins.items():
            metrics.append(f'n_crash_durations{{bin="{key}"}} {value}')
        

        content = '\n'.join(metrics) + '\n'
        return HttpResponse(content, content_type='text/plain')

def getBinRangeNameByDuration(ratio, binSize):
    return f'{ratio * binSize}-{ratio * binSize + binSize}'

def getSanitizedMessage(errorMsg):
    sanitizedMessage = ""
    errorMsgSplit = errorMsg.split(" ")
    for part in errorMsgSplit:
        if "http" not in part:
            sanitizedMessage += part

    return sanitizedMessage


