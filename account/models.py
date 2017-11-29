from django.db import models
from django.contrib.auth.models import User


class UserProfile(models.Model):
    """
    一对一关系到Django自带用户类
    增加birth和phone
    """
    user = models.OneToOneField(User, unique=True)
    birth = models.DateField(blank=True, null=True)
    phone = models.CharField(max_length=20, null=True)

    def __str__(self):
        return 'user {}'.format(self.user.username)


class UserInfo(models.Model):
    """
    用户信息
    一对一到用户类
    """
    school = models.CharField(max_length=100, blank=True)
    user = models.OneToOneField(User, unique=True)
    company = models.CharField(max_length=100, blank=True)
    profession = models.CharField(max_length=100, blank=True)
    address = models.CharField(max_length=100, blank=True)
    aboutme = models.TextField(blank=True)
    photo = models.ImageField(blank=True)

    def __str__(self):
        return 'user{}'.format(self.user.username)
