from django.conf.urls import url
from . import views

# from django.conf import settings
# ???
from django.contrib.auth import views as auth_views

urlpatterns = [
    # 旧的用户登录方式
    # url(r'^login/$',views.user_login,name='user_login'),

    # 新的用户登录注册方式，使用了django自带的函数
    url(r'^login/$', auth_views.login, {"template_name": "account/login.html"}, name="user_login"),
    url(r'logout/$', auth_views.logout, {"template_name": "account/logout.html"}, name="user_logout"),
    url(r'^register/$', views.register, name="user_register"),

    # 用户个人信息及修改个人信息的功能，图片上传
    url(r'^my-informations/$', views.myself, name='my_information'),
    url(r'^edit-my-information/$', views.myself_edit, name="edit_my_information"),
    url(r'^my-image/$', views.my_image, name="my_image"),

    # 未完成的通过email修改密码的功能
    # url(r'^password-change/$', auth_views.password_change, {"post_change_redirect": "/account/password-change-done"},
    #     name='password_change'),
    # url(r'^password-change-done/$', auth_views.password_change_done, name='password_change_done'),
    # url(r'^password-reset/$', auth_views.password_reset,
    #     {"template_name": "account/password_reset.html",
    #      "email_template_name": "account/password_reset_email.html",
    #      "subject_template_name": "/account/password_reset_subject.txt",
    #      "post_reset_redirect": "/account/password-reset-done"
    #      }, name='password_reset'),
    # url(r'^password-reset-done/$', auth_views.password_reset_done,
    #     {"template_name": "account/password_reset_done.html"},
    #     name='password_reset_done'),
    #
    # url(r'^password-reset-confirm/(?P<uidb64>[-\w]+)/(?P<token>[-\w]+)/$', auth_views.password_reset_confirm,
    #     {"template_name": "account/password_reset_confirm.html"}, name="password_reset_confirm"),
    #
    # url(r'^password-reset-complete/$', auth_views.password_reset_complete, name="password_reset_complete"),

]
