from django import template

register=template.Library()

from article.models import ArticlePost

# 使用tag后需要重启服务器
@register.simple_tag
def total_articles():
    return ArticlePost.objects.count()

@register.simple_tag
def author_total_articles(user):
    return user.article.count()