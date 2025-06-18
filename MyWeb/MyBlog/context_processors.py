from .models import Category,ArticleTag,Article
from django.db.models import Count,Sum



def sidebar_data(request):

# ============================自定义静态配置================================
    


    categories = Category.objects.annotate(post_count=Count('article'))

    total_visited = Article.objects.aggregate(total=Sum('visited_num'))['total'] or 0

    return {
        'categories':categories,
        'tags':ArticleTag.objects.all(),
        'COUNT':Article.objects.count(),
        'TOTAL_VISITED':total_visited,
        'SITE_NAME' : "IronBus 博客",
        'COPYRIGHT_OWNER' : "IronBus 团队",
        'CONTACT_EMAIL' : "814251136@qq.com",
        'ICP_BEIAN' : "备案号",
    }
