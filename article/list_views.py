'''
管理额外功能：
点赞
文章列表
文章阅读
等功能
'''
# 获取返回内容
from django.shortcuts import render,get_object_or_404,HttpResponse
# 页面管理
from django.core.paginator import Paginator,PageNotAnInteger,EmptyPage
# 基本用户管理
from django.contrib.auth.models import User
# 登录才能使用的功能
from django.contrib.auth.decorators import login_required
# 允许跨站请求（用于ajax请求）
from django.views.decorators.csrf import csrf_exempt
# 只能使用post请求
from django.views.decorators.http import require_POST

# 使用redis数据库
import redis
from django.conf import settings
from .models import ArticleColumn,ArticlePost,Comment
from .forms import CommentForm
# 为每篇文章的评论计数
from django.db.models import Count
# 连接数据库
r=redis.StrictRedis(host=settings.REDIS_HOST,port=settings.REDIS_PORT,db=settings.REDIS_DB)

# 另一个文章列表
def article_titles(request,username=None):
    '''
    于views.py不同的另一种文章列表显示方式，显示内容：article/list/author_articles.html
    :param request:这是一个http请求
    :param username:用户名
    :return:返回显示内容
    '''
    if username:
        author=User.objects.get(username=username)
        article_title=ArticlePost.objects.filter(author=author)
        try:
            userinfo=author.userinfo
        except:
            userinfo=None
    else:
        article_title=ArticlePost.objects.all()
    paginator=Paginator(article_title,2)
    page=request.GET.get('page')
    try:
        current_page=paginator.page(page)
        articles=current_page.object_list
    except PageNotAnInteger:
        current_page=paginator.page(1)
        articles=current_page.object_list
    except EmptyPage:
        current_page=paginator.page(paginator.num_pages)
        articles=current_page.object_list
    if username:
        return render(request,"article/list/author_articles.html",{"articles":articles,"page":current_page,"userinfo":userinfo,"user":author})
    return render(request,"article/list/article_titles.html",{"articles":articles,"page":current_page})

# def article_detail(request,id,slug):
#     article=get_object_or_404(ArticlePost,id=id,slug=slug)
#     total_views=r.incr("article:{}:views".format(article.id))
#     r.zincrby('article_ranking',article.id,1)
#
#     article_ranking = r.zrange('article_ranking',0,-1,desc=True)[:10]
#     article_ranking_ids=[int(id) for id in article_ranking]
#     most_viewed=list(ArticlePost.objects.filter(id__in=article_ranking_ids))
#     most_viewed.sort(key=lambda x:article_ranking_ids.index(x.id))
#     return render(request,"article/list/article_detail.html",{"article":article,"total_views":total_views,"most_viewed":most_viewed})

# 阅读文章，传入文章id，文章题目的slug url
def read_article(request,id,slug):
    article = get_object_or_404(ArticlePost, id=id, slug=slug)
    # 阅读人数+1
    total_views=r.incr("article:{}:views".format(article.id))
    # 优先等级+1
    r.zincrby('article_ranking',article.id,1)

    # 评论：
    if request.method=="POST":
        comment_form=CommentForm(data=request.POST)
        if comment_form.is_valid():
            new_comment=comment_form.save(commit=False)
            new_comment.article=article
            new_comment.save()
    # 页面请求
    else:
        comment_form=CommentForm
    # 获取文章tag的list，以列表形式返回结果
    article_tags_ids=article.article_tag.values_list("id",flat=True)
    # 找出所有文章tag相同的文章，并排除自己
    similar_articles=ArticlePost.objects.filter(article_tag__in=article_tags_ids).exclude(id=article.id)
    # 为所有相似文章添加注释并排序
    similar_articles=similar_articles.annotate(same_tags=Count("article_tag")).order_by('-same_tags','-created')[:4]
    return render(request,"article/list/article_detail.html",{"article":article,"total_views":total_views,
                                                              "comment_form":comment_form,"similar_articles":similar_articles})

# 为文章点赞的功能，ajax请求
@csrf_exempt
@login_required(login_url='/account/login/')
@require_POST
def like_article(request):
    article_id=request.POST.get("id")
    action=request.POST.get("action")
    if article_id and action:
        try:
            article=ArticlePost.objects.get(id=article_id)
            if action=="like":
                article.users_like.add(request.user)
                return HttpResponse("1")
            else:
                article.users_like.remove(request.user)
                return HttpResponse("2")
        except:
            return HttpResponse("no")



