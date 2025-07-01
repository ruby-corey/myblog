from django.contrib import admin
from .models import *

admin.site.register(About)
admin.site.register(Category)
admin.site.register(ArticleTag)
admin.site.register(Comment)


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    filter_horizontal = ('tags',)
    list_display = ('title', 'pub_date','visited_num')
    fields = ('title','cover_img','overview','category', 'tags','raw_content',)
    
    class Media:
        css = {
            'all': ('/static/MyBlog/css/mkdown.css',)  
        }
    
@admin.register(VisitRecord)
class RecordAdmin(admin.ModelAdmin):
    list_display = ('ip_address','visited_time')
    fields = ('ip_address','user_agent','visited_path','session_id', 'is_unique_today',)

@admin.register(VisitSummary)
class SummaryAdmin(admin.ModelAdmin):
    list_display = ('date',)
    fields = ('total_visits','unique_visitors','unique_ips')
    

# Register your models here.
