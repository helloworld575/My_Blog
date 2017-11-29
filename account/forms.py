from django import forms
from django.contrib.auth.models import User
from .models import UserProfile, UserInfo


class LoginForm(forms.Form):
    """
    登录所需的表单
    用户名和密码
    """
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)


class RegistrationForm(forms.ModelForm):
    """
    注册所需的表单
    用户名，密码1，密码2,
    """
    password = forms.CharField(label='密码', widget=forms.PasswordInput)
    password2 = forms.CharField(label='重复密码', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ("username", "email")

    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError("密码不匹配")
        return cd["password2"]


class UserProfileForm(forms.ModelForm):
    """
    用于注册和显示
    电话和生日
    电话必须填写
    继承（？）于UserProfile模型类
    """

    class Meta:
        model = UserProfile
        fields = ("phone", "birth")


class UserInfoForm(forms.ModelForm):
    """
    用于完善用户信息
    均不是必须的
    photo需要额外的上传
    """

    class Meta:
        model = UserInfo
        fields = ("school", "company", "profession", "address", "aboutme", "photo")


class UserForm(forms.ModelForm):
    """
    编辑个人信息时用到
    继承Django自带用户类
    """

    class Meta:
        model = User
        fields = ("email",)
