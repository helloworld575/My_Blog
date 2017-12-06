from django import template
import redis
from django.conf import settings
from django.db.models import Count
from django.utils.safestring import mark_safe
import markdown

r=redis.StrictRedis(host=settings.REDIS_HOST,port=settings.REDIS_PORT,db=settings.REDIS_DB)

register=template.Library()

from article.models import ArticlePost

# 使用tag后需要重启服务器
@register.simple_tag
def total_articles():
    return ArticlePost.objects.count()

@register.simple_tag
def author_total_articles(user):
    return user.article.count()

@register.inclusion_tag('article/list/latest_articles.html')
def latest_article(n=5):
    latest_articles=ArticlePost.objects.order_by("-created")[:n]
    return {"latest_articles":latest_articles}

@register.inclusion_tag('article/list/popular_articles.html')
def popular_articles(n=5):
    article_ranking = r.zrange('article_ranking',0,-1,desc=True)[:10]
    article_ranking_ids=[int(id) for id in article_ranking]
    most_viewed=list(ArticlePost.objects.filter(id__in=article_ranking_ids))
    most_viewed.sort(key=lambda x:article_ranking_ids.index(x.id))
    return {"most_viewed":most_viewed}

@register.assignment_tag
def comment_article(n=5):
    return ArticlePost.objects.annotate(total_comments=Count('comments')).order_by("-total_comments")[:n]

@register.filter(name='markdown')
def markdownfilter(text):
    return mark_safe(markdown.markdown(text))