# from django.shortcuts import render
# from django.http import HttpResponse
# from django.contrib.auth import authenticate,login
# from .forms import LoginForm


# def user_login(request):
#     if request.method=="POST":
#         login_form=LoginForm(request.POST)
#         if login_form.is_valid():
#             cd=login_form.cleaned_data
#             user=authenticate(username=cd['username'],password=cd['password'])
#
#             if user:
#                 login(request,user)
#                 return HttpResponse("Welcome!")
#             else:
#                 return HttpResponse("your username or password is wrong!")
#         else:
#             return HttpResponse("Invalid login")
#     if request.method=="GET":
#         login_form=LoginForm()
#         return render(request,"account/login.html",{"form":login_form})
# 以上为旧的登录功能实现，后用Django自带登录注册替代

from .forms import RegistrationForm, LoginForm, UserProfileForm, UserInfoForm, UserForm
from django.shortcuts import HttpResponse, render
from django.contrib.auth.decorators import login_required
from .models import UserProfile, UserInfo
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse


# 注册功能实现
def register(request):
    # 若为注册过程
    if request.method == "POST":
        # 调用注册表单和用户Profile表单完成
        user_form = RegistrationForm(request.POST)
        userprofile_form = UserProfileForm(request.POST)
        if user_form.is_valid():
            # 对新用户保存但不提交
            new_user = user_form.save(commit=False)
            # 调用user自带设置密码功能完成密码完善
            new_user.set_password(user_form.cleaned_data['password'])
            new_user.save()
            # 完善部分个人信息并将外键链接到new_user
            new_profiles = userprofile_form.save(commit=False)
            new_profiles.user = new_user
            new_profiles.save()
            # 保存new_user
            UserInfo.objects.create(user=new_user)
            return HttpResponseRedirect(reverse("account:user_login"))
        else:
            return render(request, "account/regisiter.html", {"form": user_form, "profile": userprofile_form,'msg':"注册失败！"})
    # 若进入注册页面
    else:
        # 调用两个form完成form的显示
        user_form = RegistrationForm()
        userprofile_form = UserProfileForm()
        return render(request, "account/regisiter.html", {"form": user_form, "profile": userprofile_form})


@login_required(login_url='/account/login')
def myself(request):
    """
    查看个人信息功能
    :param request: 查看个人信息
    :return: 个人信息页面
    """
    user = User.objects.get(username=request.user.username)
    userprofile = UserProfile.objects.get(user=user)
    userinfo = UserInfo.objects.get(user=user)
    return render(request, "account/myself.html", {"user": user, "userinfo": userinfo, "userprofile": userprofile})

@login_required(login_url='/account/login/')
def myself_edit(request):
    """
    编辑个人信息
    :param request: 请求进入页面或请求完善信息
    :return: 返回编辑页面或者返回已完成的个人信息显示
    """
    user = User.objects.get(username=request.user.username)
    userprofile = UserProfile.objects.get(user_id=request.user.id)
    userinfo = UserInfo.objects.get(user=request.user)

    if request.method == "POST":
        user_form = UserForm(request.POST)
        userprofile_form = UserProfileForm(request.POST)
        userinfo_form = UserInfoForm(request.POST)
        if user_form.is_valid() * userprofile_form.is_valid() * userinfo_form.is_valid():
            user_cd = user_form.cleaned_data
            userprofile_cd = userprofile_form.cleaned_data
            userinfo_cd = userinfo_form.cleaned_data
            user.email = user_cd['email']
            userprofile.birth = userprofile_cd['birth']
            userprofile.phone = userprofile_cd['phone']
            userinfo.school = userinfo_cd['school']
            userinfo.company = userinfo_cd['company']
            userinfo.profession = userinfo_cd['profession']
            userinfo.address = userinfo_cd['address']
            userinfo.aboutme = userinfo_cd['aboutme']
            user.save()
            userprofile.save()
            userinfo.save()
        return HttpResponseRedirect('/account/my-informations')
    else:
        user_form = UserForm(instance=request.user)
        userprofile_form = UserProfileForm(initial={"birth": userprofile.birth, "phone": userprofile.phone})
        userinfo_form = UserInfoForm(initial={"school": userinfo.school,
                                              "company": userinfo.company,
                                              "profession": userinfo.profession,
                                              "address": userinfo.address,
                                              "aboutme": userinfo.aboutme,})
        return render(request, "account/myself_edit.html", {"user_form": user_form,
                                                            "userprofile_form": userprofile_form,
                                                            "userinfo_form": userinfo_form,
                                                            "userinfo":userinfo})


@login_required(login_url='/account/login/')
def my_image(request):
    """
    上传及显示头像
    :param request: ajax请求，具体查看account/imagecrop.html，或请求显示上传页面
    :return:已完成的个人信息页面
    """
    if request.method == 'POST':
        img = request.POST['img']
        userinfo = UserInfo.objects.get(user=request.user.id)
        userinfo.photo = img
        userinfo.save()
        return HttpResponse("1")
    else:
        return render(request, 'account/imagecrop.html', )
