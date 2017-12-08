from django.contrib import admin
from .models import ArticleColumn

class ArticleColumnAdmin(admin.ModelAdmin):
    '''
    文章管理
    '''
    list_display = ('column','created','user')
    list_filter = ("column",)

admin.site.register(ArticleColumn,ArticleColumnAdmin)