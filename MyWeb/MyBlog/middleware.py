from .models import VisitRecord, VisitSummary
from django.utils import timezone

class VisitTrackingMiddleware:
    """访问统计中间件"""
    def __init__(self,get_response ):
        self.get_response = get_response 

    def __call__(self, request):
        
        excluded_paths = ['/admin/']

        if not any( request.path.startswith(path) for path in excluded_paths):
        
            VisitRecord.record_visit(request)
            today = timezone.now().date()
            
            # error
            if not VisitSummary.objects.filter(date=today).exists():            
                VisitSummary.update_summary(today)
 

        
        response = self.get_response(request)
        return response