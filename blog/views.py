from django.shortcuts import render,get_object_or_404
from .models import BlogArticles,User
from django.contrib.auth.decorators import login_required


@login_required(login_url='/account/login/')
def blog_title(request):
    user = User.objects.get(username=request.user.username)
    blogs = BlogArticles.objects.filter(author=user)
    return render(request, "blog/titles.html", {"blogs": blogs})

@login_required(login_url='/account/login/')
def blog_article(request,article_id):
    # article=BlogArticles.objects.get(id=article_id)
    article=get_object_or_404(BlogArticles,id=article_id)
    pub=article.publish
    return render(request,"blog/content.html",{"article":article,"publish":pub})


