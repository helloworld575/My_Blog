from django.shortcuts import render,get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from django.views.decorators.http import require_POST
from django.core.paginator import Paginator,EmptyPage,PageNotAnInteger

from .forms import ArticleColumnForm,ArticlePostForm,ArticleTagForm
from .models import ArticleColumn,ArticlePost,ArticleTag
# 使用python标准json库
import json

# 文章栏目管理,可ajax,需登录
@login_required(login_url='/account/login/')
@csrf_exempt
def article_column(request):
    if request.method=="GET":
        # 获取文章所有栏目
        columns=ArticleColumn.objects.filter(user=request.user)
        column_form=ArticleColumnForm()
        return render(request,"article/column/article_column.html",{"columns":columns,"column_form":column_form})
    elif request.method=="POST":
        # 提交文章栏目(新增)
        column_name=request.POST['column']
        columns=ArticleColumn.objects.filter(user_id=request.user.id,column=column_name)
        if columns:
            return HttpResponse('2')
        else:
            ArticleColumn.objects.create(user=request.user,column=column_name)
            return HttpResponse('1')

# 编辑栏目名称,可ajax,需登录,且使用post方式
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

# 删除栏目,同上
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

# 发布文章,ajax提交,必须登录
@login_required(login_url='/account/login')
@csrf_exempt
def article_post(request):
    if request.method=="POST":
        # 发布文章
        article_post_form=ArticlePostForm(request.POST)
        if article_post_form.is_valid():
            cd = article_post_form.cleaned_data
            try:
                new_article=article_post_form.save(commit=False)
                new_article.author=request.user
                new_article.column=request.user.article_column.get(id=request.POST['column_id'])
                new_article.save()
                tags=request.POST['tags']
                if tags:
                    for atag in json.loads(tags):
                        tag=request.user.tag.get(tag=atag)
                        new_article.article_tag.add(tag)
                return HttpResponse("1")
            except:
                return HttpResponse("2")
        else:
            return HttpResponse("3")
    else:
        # 进入发布文章页面
        article_post_form=ArticlePostForm()
        article_column=request.user.article_column.all()
        article_tags=request.user.tag.all()
        return render(request,"article/column/article_post.html",{"article_post_form":article_post_form,"article_column":article_column,"tags":article_tags})

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

# 查看文章
@login_required(login_url='/account/login')
def article_detail(request,article_id,slug):
    article=get_object_or_404(ArticlePost,id=article_id,slug=slug)
    return render(request,'article/column/article_detail.html',{"article":article})

# 删除文章
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

# 编辑文章
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

# 新建文章tag
@login_required(login_url='/account/login')
@csrf_exempt
def article_tag(request):
    if request.method=="GET":
        article_tags=ArticleTag.objects.filter(author=request.user)
        article_tag_form=ArticleTagForm()
        return render(request,"article/tag/tag_list.html",{"article_tags":article_tags,"article_tag_form":article_tag_form})
    if request.method=="POST":
        tag_post_form=ArticleTagForm(data=request.POST)
        if tag_post_form.is_valid():
            try:
                new_tag=tag_post_form.save(commit=False)
                new_tag.author=request.user
                new_tag.save()
                return HttpResponse("1")
            except:
                return HttpResponse("2")
        else:
            return HttpResponse("3")

# 删除tag
@login_required(login_url='/account/login')
@csrf_exempt
@require_POST
def delete_tag(request):
    tag_id=request.POST['tag_id']
    try:
        tag=ArticleTag.objects.get(id=tag_id)
        tag.delete()
        return HttpResponse("1")
    except:
        return HttpResponse("2")