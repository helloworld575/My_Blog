from django.shortcuts import render,get_object_or_404,HttpResponse
from django.core.paginator import Paginator,PageNotAnInteger,EmptyPage
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST

from .models import ArticleColumn,ArticlePost

# 另一个文章列表
def article_titles(request,username=None):
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

def article_detail(request,id,slug):
    article=get_object_or_404(ArticlePost,id=id,slug=slug)
    return render(request,"article/list/article_detail.html",{"article":article})

@csrf_exempt
@login_required(login_url='/account/login/')
# @require_POST
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