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

from .forms import RegistrationForm,LoginForm,UserProfileForm
from django.shortcuts import HttpResponse,render


def register(request):
    if request.method=="POST":
        user_form=RegistrationForm(request.POST)
        userprofile_form=UserProfileForm(request.POST)
        if user_form.is_valid():
            new_user=user_form.save(commit=False)
            new_user.set_password(user_form.cleaned_data['password'])
            new_user.save()
            new_profiles=userprofile_form.save(commit=False)
            new_profiles.user=new_user
            new_profiles.save()
            return HttpResponse("successfully")
        else:
            return HttpResponse("sorry you can not regisiter")
    else:
        user_form=RegistrationForm()
        userprofile_form=UserProfileForm()
        return render(request,"account/regisiter.html",{"form":user_form,"profile":userprofile_form})