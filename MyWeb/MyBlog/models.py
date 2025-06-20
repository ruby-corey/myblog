from django.db import models
from django.db.models import F
from markdownx.models import MarkdownxField
import markdown
import bleach
from PIL import Image
from django.utils import timezone
# Create your models here.

class Category(models.Model):
    """ 分类 """
    name = models.CharField(max_length=100,unique=True)
    # 搜索优化
    slug = models.SlugField(max_length=100,unique=True)

    class Meta:
        verbose_name = "文章分类"
        verbose_name_plural = "文章分类"

    def __str__(self):
        return self.name
    
class ArticleTag(models.Model):
    """ 标签 """
    name = models.CharField(max_length=100,unique=True)
    # 搜索优化
    slug = models.SlugField(max_length=100,unique=True)
        
    class Meta:
        verbose_name = "文章标签"
        verbose_name_plural = "文章标签"

    def __str__(self):
        return self.name

class Article(models.Model):
    """ 文章 """
    # 标题概述
    title = models.CharField(max_length=200)
    overview = models.TextField(max_length=300,default='',blank=True,verbose_name="概述")

    # 分类标签
    category = models.ForeignKey(Category,null=True,blank=True,on_delete=models.SET_NULL,verbose_name="分类",related_name='article')
    tags = models.ManyToManyField(ArticleTag,blank=True,verbose_name="标签")
    # ManyToManyField是个queryset，尚未执行数据库查询（例如使用了延迟加载），其布尔值可能暂时为 True，判断可以用exists
    # 文章内容
    raw_content = MarkdownxField(verbose_name="Markdown原始内容")
    rendered_content = models.TextField(verbose_name="渲染后的html",editable=False)
    version = models.PositiveIntegerField(default=1)
    
    # 发布更新时间。
    pub_date = models.DateTimeField("发布时间",auto_now_add=True)
    last_updated = models.DateTimeField("最后更新", auto_now=True)

    # 统计
    word_count = models.PositiveIntegerField(default=0,verbose_name="字数",editable=False)
    visited_num = models.PositiveIntegerField(default=0,verbose_name="访问量",editable=False)
    
    cover_img = models.ImageField(upload_to="article_cover/",null=True,blank=True,verbose_name="文章封面")

    class Meta:
        verbose_name = "文章"
        verbose_name_plural = "文章"
        ordering = ['-pub_date']

    def increase_visited(self):
        """ 访问量增加 """
        Article.objects.filter(pk=self.pk).update(visited_num=F("visited_num")+1)
        self.refresh_from_db(fields=['visited_num'])

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        """ 计数 """
        CNwords = sum(1 for char in self.raw_content if '\u4e00' <= char <= '\u9fff')
        NonCNwords = [word for word in self.raw_content.split() if not any('\u4e00' <= char <= '\u9fff' for char in word)]
        self.word_count = CNwords + len(NonCNwords)

        """
            Markdown转换:
                --存储与展示分离:
                    1.原始内容:保留易编辑的Markdown格式(适合后台管理)
                    2.渲染内容:生成可直接展示的HTML(提升前端性能)
        """
        if not self.pk or Article.objects.get(pk=self.pk).raw_content != self.raw_content:
            html = markdown.markdown(self.raw_content, 
                    extensions=[
                    'extra',       # 启用表格、目录等扩展功能
                    #'toc',目录
                    #'codehilite',   代码语法高亮支持,还要配置HTML文件，设置css和js文件
                    ]
                )
            
            """
                HTML净化:
                    1.防御XSS攻击:防止用户插入恶意脚本
                    2.内容可控性:限制允许的HTML标签和属性
            """
            self.rendered_content = bleach.clean(
                    html,  # 待净化的原始HTML
                    # 白名单标签
                    tags=[
                        'p', 'h1', 'h2', 'h3','h4','h5','h6'      # 基础文本结构
                        'ul', 'li', 'ol',            # 列表
                        'pre', 'code', 'blockquote',         # 代码块
                        'blockquote',           # 引用
                        'img', 'a', 'strong', 'em',
                        'table', 'thead', 'tbody', 'tr', 'th', 'td'                 # 图片
                    ],
                    # 允许的属性（按标签过滤）
                    attributes={
                        'img': [
                            'src',    # 图片地址
                            'alt',    # 替代文本
                            'title'  # 悬浮提示
                        ],
                        'a': ['href', 'title', 'rel'],
                        'code': ['class']
                    }
                )
        
            if self.pk:
                self.version +=1

        super().save(*args, **kwargs)

class Comment(models.Model):
    """
        评论
    """
    article = models.ForeignKey(Article, on_delete=models.CASCADE, verbose_name="关联文章",related_name="comments")
    comment_date = models.DateTimeField("评论时间", auto_now_add=True,null=True, blank=True )
    body = models.CharField(max_length=500,default='',verbose_name="评论内容")
    author = models.CharField(max_length=100,default="匿名用户",verbose_name="用户")
    email = models.EmailField(verbose_name='邮箱(不会公开)', blank=True)
    #审核状态
    #is_approved = models.BooleanField(default=False,verbose_name="审核通过")

    class Meta:
        verbose_name = "评论"
        verbose_name_plural = "评论"
        ordering = ['-comment_date']

    def __str__(self):
        return f"{self.author}的评论：{self.body[:20]}"
    
    def save(self, *args, **kwargs):
        """确保新评论有创建时间"""
        if not self.pk and not self.comment_date:  # 新记录且没有创建时间
            self.comment_date = timezone.now()
        super().save(*args, **kwargs)

class About(models.Model):
    """关于"""
    title = models.CharField(max_length=200,default="关于我们")
    content = models.TextField(verbose_name="内容")
    slug = models.SlugField(unique=True, default='about-page')

    def __str__(self):
        return self.title
    
class VisitRecord(models.Model):
    " 访问记录 "
    ip_address = models.GenericIPAddressField(verbose_name="IP地址")
    user_agent = models.TextField(verbose_name="用户代理",max_length=500,blank=True,null=True)
    visited_time = models.DateTimeField(verbose_name="访问时间",auto_now_add=True)
    visited_path = models.CharField(verbose_name="访问路径",max_length=200)
    session_id = models.CharField(verbose_name="会话ID",max_length=40,blank=True,null=True)
    is_unique_today = models.BooleanField(verbose_name="今日唯一时间",default=False)

    class Meta:
        verbose_name = "访问记录"
        verbose_name_plural = "访问记录"
        indexes = [
            models.Index(fields=['ip_address','visited_time']),
            models.Index(fields=['session_id','visited_time']),
            models.Index(fields=['visited_time']),
        ]

    @staticmethod
    def get_client_ip(request):
        x_forward_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forward_for:
            ip = x_forward_for.split(',')[0].strip()
        else:
            ip = request.META.get('REMOTE_ADDR','0.0.0.0')
        return ip
    
    @classmethod
    def record_visit(cls,request,ip=None):
        if ip is None:
            ip = cls.get_client_ip(request)

        user_agent = request.META.get('HTTP_USER_AGENT', '')[:500]
        visited_path = request.path[:200]
        session_id = request.session.session_key

        if not session_id:
            request.session.create()
            session_id = request.session.session_key
        
        today = timezone.now().date()
        existing_today = cls.objects.filter(
            visited_time__date=today,
            user_agent=user_agent,
            ip_address=ip
        ).exists()

        record = cls.objects.create(
            ip_address=ip,
            user_agent=user_agent,
            visited_time=timezone.now(),
            visited_path=visited_path,
            session_id=session_id,
            is_unique_today=not existing_today
        )

        return record
    
class VisitSummary(models.Model):
    " 访问统计 "
    date = models.DateField(unique=True, verbose_name="日期")
    total_visits = models.IntegerField(default=0, verbose_name="总访问量")
    unique_visitors = models.IntegerField(default=0, verbose_name="唯一访客数")
    unique_ips = models.IntegerField(default=0, verbose_name="唯一IP数")
    # most_visited_path = models.CharField(max_length=200, blank=True, null=True, verbose_name="最热门路径")
    # visits_by_hour = models.JSONField(default=dict, verbose_name="按小时访问分布")
    
    class Meta:
        verbose_name = "访问统计摘要"
        verbose_name_plural = "访问统计摘要"
    
    @classmethod
    def update_summary(cls,date=None):
        if date is None:
            date = timezone.now().date()

        records = VisitRecord.objects.filter(visited_time__date=date)
        
        total_visits = records.count()
        unique_visitors = records.filter(is_unique_today=True).count()
        unique_ips = records.values('ip_address').distinct().count()

        summary, created = cls.objects.update_or_create(
                date=date,
                defaults={
                    'total_visits': total_visits,
                    'unique_visitors': unique_visitors,
                    'unique_ips': unique_ips,
                }
            )
            
        return summary
