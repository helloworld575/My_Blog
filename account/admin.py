from django.contrib import admin
from .models import UserProfile
from .models import UserInfo


class UserProfileAdmin(admin.ModelAdmin):
    """
    管理界面显示用户生日和电话
    电话是必须的，生日可以不填
    """
    list_display = ('user', 'birth', 'phone')
    list_filter = ("phone",)


class UserInfoAdmin(admin.ModelAdmin):
    """
    管理界面显示用户个人信息
    无法显示图片
    """
    list_display = ('user', 'school', 'company', 'profession', 'address', 'aboutme', 'photo')
    list_filter = ("school", "company", "profession")


admin.site.register(UserInfo, UserInfoAdmin)
admin.site.register(UserProfile, UserProfileAdmin)
