from django.urls import path
from . import views



app_name = "MyBlog"
urlpatterns = [
    
    path("",views.article_list,name="home"),
    path("article/<int:pk>/",views.commentview,name="article_detail"),
    path("archive/tag/<slug:tag_slug>/",views.ArriveAtView.as_view(),name="arrived-by-tag"),
    path("archive/category/<slug:cat_slug>/",views.ArriveAtView.as_view(),name="arrived-by-category"),
    path("archive/",views.ArchiveView.as_view(),name="archive"),
    path('about/<slug:slug>/', views.AboutDetailView.as_view(), name='about'),
    path("search/",views.SearchView.as_view(),name="search"),

    
    
]