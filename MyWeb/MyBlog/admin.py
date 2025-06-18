from django.contrib import admin
from .models import *

admin.site.register(About)
admin.site.register(Category)
admin.site.register(ArticleTag)
admin.site.register(Comment)

@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    filter_horizontal = ('tags',)
    list_display = ('title', 'pub_date','rendered_content','visited_num')
    fields = ('title','cover_img','overview','category', 'tags','raw_content',)
# Register your models here.
