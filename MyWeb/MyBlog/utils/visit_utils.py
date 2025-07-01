from MyBlog.models import VisitRecord,VisitSummary
from django.utils import timezone
from django.http import HttpRequest
from django.conf import settings
from django.db import transaction
from django.utils import timezone
from .ip_utils import get_client_ip




def get_local_date():
    """获取当前本地日期"""
    local_time = timezone.localtime(timezone.now())
    return local_time.date()

def record_visit(request: HttpRequest, ip= None):
    if ip is None:
        ip = get_client_ip(request)

    user_agent = request.META.get('HTTP_USER_AGENT', '')[:500]
    visited_path = request.path[:200]
    session_id = request.session.session_key

    if not session_id:
        request.session.create()
        session_id = request.session.session_key

    now = timezone.now().date()

    existing_today = VisitRecord.objects.filter(
        visited_time__date=now,
        session_id=session_id,  
    ).exists()

    record = VisitRecord.objects.create(
        ip_address=ip,
        user_agent=user_agent,
        visited_time=now,  
        visited_path=visited_path,
        session_id=session_id,
        is_unique_today=not existing_today
    )

    return record

def update_summary(date = None):
    if date is None:
        
        date =timezone.now().date()

    # 构造带时区的日期范围(问题所在这时的date)
    # 这种方式显式构造了带时区的完整日期范围（从当天 0 点到 23:59:59），避免了数据库自动时区转换可能带来的问题。
    start_time = timezone.make_aware(
        timezone.datetime.combine(date, timezone.datetime.min.time()),
        timezone.get_current_timezone()
    )
    end_time = timezone.make_aware(
        timezone.datetime.combine(date, timezone.datetime.max.time()),
        timezone.get_current_timezone()
    )
    #----------------------------------------
    records = VisitRecord.objects.filter(visited_time__range=(start_time, end_time))
    total_visits = records.count()
    unique_visitors = records.values('session_id').distinct().count()  
    unique_ips = records.values('ip_address').distinct().count()

    summary, created = VisitSummary.objects.update_or_create(
        date=date,
        defaults={
            'total_visits': total_visits,
            'unique_visitors': unique_visitors,
            'unique_ips': unique_ips,
        }
    )
            
    return summary
    