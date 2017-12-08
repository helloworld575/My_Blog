from django.conf.urls import url
from . import views,list_views

urlpatterns=[
    # 文章栏目(自我分类)
    url(r'^article-column/$', views.article_column, name="article_column"),
    # 删除栏目
    url(r'^del-column/$',views.del_column,name="del_column"),
    # 编辑栏目
    url(r'^rename-column/$',views.rename_column,name="rename_column"),
    # 上传文章
    url(r'^article-post/$',views.article_post,name="article_post"),
    # 获取文章列表
    url(r'^article-list/$',views.article_list,name="article_list"),
    # 查看文章
    url(r'^article-detail/(?P<article_id>\d+)/(?P<slug>[-\w]+)/$',views.article_detail,name="article_detail"),
    # 删除文章
    url(r'^del-article/$',views.del_article,name="del_article"),
    # 编辑文章
    url(r'^edit-article/(?P<article_id>\d+)/$',views.edit_article,name="redit_article"),\
    # 查看list文章题目列表
    url(r'^list-article-titles/$',list_views.article_titles,name="article_titles"),
    # 查看list文章内容
    url(r'^list-article-detail/(?P<id>\d+)/(?P<slug>[-\w]+)/$',list_views.read_article,name="list_article_detail"),
    # 获取作者全部文章
    url(r'^author-articles/(?P<username>[-\w]+)/$',list_views.article_titles,name="author_articles"),
    # 点赞文章
    url(r'^like-article/$',list_views.like_article,name="like_article"),
    # 文章tag设置
    url(r'^article-tags/$',views.article_tag,name="article_tags"),
    # 删除tag
    url(r'^del-tag/$',views.delete_tag,name="del_tag"),
]