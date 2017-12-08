'''
此包用于管理tags
使用tag后需要重启服务器
tag的调用方法见templates/article/tag/tag_list.html
有三种自定义模板标签类型方式:simple_tag,inclusion_tag,assignment_tag
'''

# 调用tags
from django import template
#使用redis数据库
import redis
# 使用settings中的变量
from django.conf import settings
# 为每篇文章的评论计数
from django.db.models import Count
# 用于解析markdown句法，暂时没有运行
from django.utils.safestring import mark_safe
import markdown
# 链接redis数据库
r=redis.StrictRedis(host=settings.REDIS_HOST,port=settings.REDIS_PORT,db=settings.REDIS_DB)
# 链接template中的tag库
register=template.Library()
# 引入ArticlePost模块
from article.models import ArticlePost

# 返回所有文章个数
@register.simple_tag
def total_articles():
    return ArticlePost.objects.count()

# 返回作者文章总数
@register.simple_tag
def author_total_articles(user):
    return user.article.count()

# 返回最新文章，tag本身在html中
@register.inclusion_tag('article/list/latest_articles.html')
def latest_article(n=5):
    latest_articles=ArticlePost.objects.order_by("-created")[:n]
    return {"latest_articles":latest_articles}

# 获取最多查看的文章
@register.inclusion_tag('article/list/popular_articles.html')
def popular_articles(n=5):
    # 调用redis数据库（name，start，end，？？）前十
    article_ranking = r.zrange('article_ranking',0,-1,desc=True)[:10]
    # 获取这些article的id
    article_ranking_ids=[int(id) for id in article_ranking]
    # 获取全部articles
    most_viewed=list(ArticlePost.objects.filter(id__in=article_ranking_ids))
    # 将articles排序
    most_viewed.sort(key=lambda x:article_ranking_ids.index(x.id))
    return {"most_viewed":most_viewed}

# 获取评论数最多的文章
@register.assignment_tag
def comment_article(n=5):
    '''
    annotate为所有文章对象添加注释,注释内容是当前文章的所有评论数量,并根据评论数排序
    :param n: 排最先的数量
    :return: 返回article对象的集合
    '''
    return ArticlePost.objects.annotate(total_comments=Count('comments')).order_by("-total_comments")[:n]

# markdown模板,输入markdown模板内容,输出经markdown返回后的结果,返回名称为markdown,具体查看templates/article/list/article_detail.html
@register.filter(name='markdown')
def markdownfilter(text):
    return mark_safe(markdown.markdown(text))