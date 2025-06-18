from django.shortcuts import render,get_object_or_404,redirect
from django.http import HttpResponse
from django.views import generic
from .models import *
from django.db.models import Count,Q
from django.core.paginator import Paginator,EmptyPage,PageNotAnInteger
from .forms import CommentForm
from django.db.models.functions import TruncMonth

# ===================基础样式=================================================
# class IndexView(generic.ListView):
#     """
#         首页
#     """
#     model = Article
#     template_name = "blog/home.html"
#     def get_queryset(self):
#         """Return the last five published questions."""
#         return Article.objects.all()

# class ArticleDetailView(generic.DetailView):
#     """文章内容"""
#     model = Article
#     template_name = "blog/article_detail.html"
# =============================文章列表=======================================

def article_list(request):
    articles = Article.objects.all().order_by('-pub_date').prefetch_related('tags')
    paginator = Paginator(articles,8)
    page = request.GET.get('page')
    
    try:
        article_page = paginator.page(page)
    except PageNotAnInteger:
        article_page = paginator.page(1)
    except EmptyPage:
        article_page = paginator.page(paginator.num_pages)
    

    context = {
        'articles':article_page,
    }
    return render(request,'blog/article_list.html',context)
# ================================标签分类跳转页=========================================
class ArriveAtView(generic.ListView):
    model = Article
    context_object_name = 'articles'
    template_name = 'blog/arrived.html'
    paginate_by = 8
    
    def is_request_tag(self):
        
        return self.request.path.startswith('/MyBlog/archive/tag/')
    
    def is_request_cate(self):

        return self.request.path.startswith('/MyBlog/archive/category/')
    
    def get_queryset(self):
        
        # print("请求路径:", self.request.path)
        # print("URL参数:", self.kwargs)
        tag_slug = self.kwargs.get('tag_slug')
        cat_slug = self.kwargs.get('cat_slug')

        if self.is_request_tag() and tag_slug:

            tag = get_object_or_404(ArticleTag, slug=tag_slug)
            self.current_filter = 'tag'
            self.current_slug = tag_slug
            
            return Article.objects.filter(tags=tag).prefetch_related('tags', 'category')
        
        elif self.is_request_cate() and cat_slug:

            category = get_object_or_404(Category, slug=cat_slug)
            
            self.current_filter = 'category'
            self.current_slug = cat_slug
            return Article.objects.filter(category=category).prefetch_related('tags', 'category')
        
        else:
            
            return Article.objects.none()
        
    
    def get_context_data(self, **kwargs):
        
        
        context = super().get_context_data(**kwargs)
        if hasattr(self,'current_filter'):
            if self.current_filter == 'tag':
                context['current_task'] = get_object_or_404(ArticleTag,slug=self.current_slug)
            elif self.current_filter == 'category':
                context['current_task'] = get_object_or_404(Category,slug=self.current_slug)

        return context

# =====================================评论视图===============================================
def commentview(request,pk):

    article = get_object_or_404(Article,pk=pk)
    article.increase_visited()
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.article = article
            comment.save()
            # 不做重定向的话，页面会重复提交表单且跳转到页面顶部
            return redirect(f'{request.path}#comment-section')
    else:
        form = CommentForm()

    comments = article.comments.all()
    total_cmt = comments.count()
    for i,cmt in enumerate(comments,start=1):
        cmt.floor = total_cmt - i + 1

    context = {
        'article': article,
        'comments': comments,
        'form': form,
    }
    
    return render(request, 'blog/article_detail.html', context)
# =======================================搜索==================================================
class SearchView(generic.ListView):

    model = Article
    template_name = "blog/search.html"
    context_object_name = "articles"
    paginate_by = 8

    def get_queryset(self):

        query = self.request.GET.get('q','')
        if query:

            return Article.objects.filter(
                Q(title__icontains=query) |
                Q(overview__icontains=query) |
                Q(raw_content__icontains=query)
            ).distinct().order_by('-pub_date')
        
        return Article.objects.none()
    
    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)
        context['query'] = self.request.GET.get('q','')

        return context
# =======================================归档======================================================

class ArchiveView(generic.ListView):
    model = Article
    template_name = "blog/archive.html"
    context_object_name = "archive_data"

    def get_queryset(self):
        
        articles = Article.objects.order_by('-pub_date')
        
        year_month_data = {}
        
        for article in articles:
            pub_date = article.pub_date
            year = pub_date.year
            month = pub_date.month
            
           
            if year not in year_month_data:
                year_month_data[year] = {}
            
            
            if month not in year_month_data[year]:
                year_month_data[year][month] = []
            
            
            year_month_data[year][month].append(article)
        
       
        archive_data = []
        for year in sorted(year_month_data.keys(), reverse=True):
            year_articles = year_month_data[year]
            year_total = 0
            month_list = []
            
            for month in sorted(year_articles.keys(), reverse=True):
                month_articles = year_articles[month]
                month_total = len(month_articles)
                year_total += month_total
                
                month_list.append({
                    'month': month,
                    'articles': month_articles,
                    'ycount': month_total
                })
            
            archive_data.append({
                'year': year,
                'months': month_list,
                'total_count': year_total
            })
        
        return archive_data
    
# =======================================关于======================================================

class AboutDetailView(generic.DetailView):
    """关于我们"""
    model = About
    slug_field = "slug"  
    slug_url_kwarg = "slug" 
    template_name = "blog/about.html"



