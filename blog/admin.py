from django.contrib import admin
from .models import BlogArticles


class BlogArticleAdmin(admin.ModelAdmin):
    list_display = ("title", "author", "publish")
    # 显示表格内容

    list_filter = ("publish", "author")
    # 过滤器（左侧）

    search_fields = ("title", "body")
    # 上方搜索栏

    raw_id_fields = ("author",)
    # 修改作者时可通过搜索id

    date_hierarchy = "publish"
    # 导航栏显示日期

    ordering = ['publish', 'author']
    # 讲道理应该是排序


admin.site.register(BlogArticles, BlogArticleAdmin)
