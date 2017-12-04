from django.shortcuts import render,get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from django.views.decorators.http import require_POST
from django.core.paginator import Paginator,EmptyPage,PageNotAnInteger

from .forms import ArticleColumnForm,ArticlePostForm
from .models import ArticleColumn,ArticlePost


@login_required(login_url='/account/login/')
@csrf_exempt
def article_column(request):
    if request.method=="GET":
        columns=ArticleColumn.objects.filter(user=request.user)
        column_form=ArticleColumnForm()
        return render(request,"article/column/article_column.html",{"columns":columns,"column_form":column_form})
    elif request.method=="POST":
        column_name=request.POST['column']
        columns=ArticleColumn.objects.filter(user_id=request.user.id,column=column_name)
        if columns:
            return HttpResponse('2')
        else:
            ArticleColumn.objects.create(user=request.user,column=column_name)
            return HttpResponse('1')

@login_required(login_url='/account/login/')
@csrf_exempt
@require_POST
def rename_column(request):
    column_name=request.POST['column_name']
    column_id=request.POST['column_id']
    try:
        line=ArticleColumn.objects.get(id=column_id)
        line.column=column_name
        line.save()
        return HttpResponse("1")
    except:
        return HttpResponse("0")

@login_required(login_url='/account/login/')
@csrf_exempt
@require_POST
def del_column(request):
    column_id=request.POST['column_id']
    try:
        line=ArticleColumn.objects.get(id=column_id)
        line.delete()
        return HttpResponse("1")
    except:
        return HttpResponse("2")

@login_required(login_url='/account/login')
@csrf_exempt
def article_post(request):
    if request.method=="POST":
        article_post_form=ArticlePostForm(request.POST)
        if article_post_form.is_valid():
            cd = article_post_form.cleaned_data
            try:
                new_article=article_post_form.save(commit=False)
                new_article.author=request.user
                new_article.column=request.user.article_column.get(id=request.POST['column_id'])
                new_article.save()
                return HttpResponse("1")
            except:
                return HttpResponse("2")
        else:
            return HttpResponse("3")
    else:
        article_post_form=ArticlePostForm()
        article_column=request.user.article_column.all()
        return render(request,"article/column/article_post.html",{"article_post_form":article_post_form,"article_column":article_column})

@login_required(login_url='/account/login')
def article_list(request):
    """
    为控制article分页，主要部分在templates/paginator.html页面中
    :param request:
    :return:
    """
    articles_list=ArticlePost.objects.filter(author=request.user)
    # 创建分页对象，每页最大数量为2
    paginator=Paginator(articles_list,2)
    # 获取当前page的值
    page=request.GET.get('page')
    try:
        # page()得到指定页面（当前）内容，参数必须为大于等于一的整数
        current_page=paginator.page(page)
        # object_list为Page对象的属性，得到该页所有对象列表
        articles=current_page.object_list
    # 若不是整数
    except PageNotAnInteger:
        current_page=paginator.page(1)
        articles=current_page.object_list
    # 若参数为空或没有page参数
    except EmptyPage:
        current_page=paginator.page(paginator.num_pages)
        articles=current_page.object_list
    return render(request, 'article/column/article_list.html',{"articles":articles,"page":current_page})

@login_required(login_url='/account/login')
def article_detail(request,article_id,slug):
    article=get_object_or_404(ArticlePost,id=article_id,slug=slug)
    return render(request,'article/column/article_detail.html',{"article":article})

@login_required(login_url='/account/login')
@csrf_exempt
@require_POST
def del_article(request):
    article_id=request.POST["article_id"]
    try:
        article=ArticlePost.objects.get(id=article_id)
        article.delete()
        return HttpResponse("1")
    except:
        return HttpResponse("2")


@login_required(login_url='/account/login')
@csrf_exempt
def edit_article(request,article_id):
    if request.method=="GET":
        article_columns=request.user.article_column.all()
        # article=ArticlePost.objects.get(id=article_id)
        article=get_object_or_404(ArticlePost,id=article_id)
        this_article_form=ArticlePostForm(initial={"title":article.title})
        this_article_column=article.column
        return render(request,'article/column/redit_article.html',{"article":article,"article_columns":article_columns,"this_article_form":this_article_form,"this_article_column":this_article_column})
    else:
        redit_article=ArticlePost.objects.get(id=article_id)
        try:
            redit_article.column=request.user.article_column.get(id=request.POST['column_id'])
            redit_article.title=request.POST['title']
            redit_article.body=request.POST['body']
            redit_article.save()
            return HttpResponse("1")
        except:
            return HttpResponse("2")
