from .models import VisitRecord, VisitSummary
from django.utils import timezone
from MyBlog.utils.visit_utils import *

import logging
logger = logging.getLogger(__name__)

class VisitTrackingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.excluded_ips = [
            '127.0.0.1',
            '124.79.161.138'
            # 内网IP
            # CIDR网段
        ]
    def __call__(self, request):
        
        logger.info(f"中间件触发路径: {request.path}")
        ip = get_client_ip(request)
        is_ip_excluded = ip in self.excluded_ips

        excluded_paths = ['/admin/']
        is_path_excluded = any(request.path.startswith(path) for path in excluded_paths)

        if is_path_excluded or is_ip_excluded:
            logger.info(f"IP {ip} 或路径 {request.path} 被排除，跳过记录")
            return self.get_response(request)
        
        
        try:
            ip = get_client_ip(request)
            logger.info(f"记录访问IP: {ip}, 路径: {request.path}")
            
            
            record_visit(request)

            now = timezone.now().date()
            

            logger.info(f">>中间件日期: {now}")
            update_summary(now)
            

        except Exception as e:
            logger.error(f"记录访问失败: {str(e)}", exc_info=True)
        
        response = self.get_response(request)
        return response