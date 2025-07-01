from .models import *
from django.db.models import Count,Sum
from django.utils import timezone



def sidebar_data(request):


    categories = Category.objects.annotate(post_count=Count('article'))
    total_visited = Article.objects.aggregate(total=Sum('visited_num'))['total'] or 0

    total_visitors = VisitSummary.objects.aggregate(total=Sum('total_visits'))['total'] or 0
    unique_visitors = VisitSummary.objects.aggregate(total=Sum('unique_visitors'))['total'] or 0
    unique_ips = VisitSummary.objects.aggregate(total=Sum('unique_ips'))['total'] or 0
    
    data_dic = {
        'categories':categories,
        'tags':ArticleTag.objects.all(),
        'COUNT':Article.objects.count(),
        'TOTAL_READERS':total_visited,
        'TOTAL_VISITORS': unique_ips,
        'TOTAL_UNIQUE_VISITORS': unique_visitors, 
        'SITE_NAME' : "铁行驿",
        'COPYRIGHT_OWNER' : "IronBus",
        'CONTACT_EMAIL' : "814251136@qq.com",
        'ICP_BEIAN' : "备案号",
    }

    return data_dic
