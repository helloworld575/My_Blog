from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.core.urlresolvers import reverse
# 用于article获取url
from slugify import slugify

# 文章栏目对象
class ArticleColumn(models.Model):
    user=models.ForeignKey(User,related_name='article_column')
    column=models.CharField(max_length=200)
    created=models.DateField(auto_now=True)

    def __str__(self):
        return self.column

# 文章标签对象
class ArticleTag(models.Model):
    author=models.ForeignKey(User,related_name='tag')
    tag = models.CharField(max_length=500)

    def __str__(self):
        return self.tag

# 文章对象
class ArticlePost(models.Model):
    author=models.ForeignKey(User,related_name='article')
    title=models.CharField(max_length=200)
    slug=models.SlugField(max_length=500)
    column=models.ForeignKey(ArticleColumn,related_name="article_column")
    body=models.TextField()
    created=models.DateTimeField(default=timezone.now())
    updated=models.DateTimeField(auto_now=True)
    users_like=models.ManyToManyField(User,related_name="articles_like",blank=True)
    article_tag=models.ManyToManyField(ArticleTag,related_name='article_tag',blank=True)

    class Meta:
        ordering=("title",)
        index_together=(('id','slug'))

    def __str__(self):
        return self.title

    # 保存文章对象（slug额外保存）
    def save(self,*args,**kwargs):
        self.slug=slugify(self.title)
        super(ArticlePost,self).save(*args,**kwargs)

    # slug获取url
    def get_absolute_url(self):
        return reverse("article:article_detail",args=[self.id,self.slug])

    # slug获取url
    def get_url_path(self):
        return reverse("article:list_article_detail",args=[self.id,self.slug])

# 评论对象
class Comment(models.Model):
    article=models.ForeignKey(ArticlePost,related_name="comments")
    commentator=models.CharField(max_length=90)
    body=models.TextField()
    created=models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering=('-created',)

    def __str__(self):
        return "comment by {0} on {1}".format(self.commentator,self.article)

