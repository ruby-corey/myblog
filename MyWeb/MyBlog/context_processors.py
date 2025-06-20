from .models import *
from django.db.models import Count,Sum



def sidebar_data(request):


    categories = Category.objects.annotate(post_count=Count('article'))
    total_visited = Article.objects.aggregate(total=Sum('visited_num'))['total'] or 0
    total_visitors = VisitSummary.objects.aggregate(visitors=Sum('total_visits'))['visitors'] or 0

    data_dic = {
        'categories':categories,
        'tags':ArticleTag.objects.all(),
        'COUNT':Article.objects.count(),
        'TOTAL_READERS':total_visited,
        'TOTAL_VISITORS': total_visitors,
        'SITE_NAME' : "IronBus 博客",
        'COPYRIGHT_OWNER' : "IronBus 团队",
        'CONTACT_EMAIL' : "814251136@qq.com",
        'ICP_BEIAN' : "备案号",
    }

    return data_dic
