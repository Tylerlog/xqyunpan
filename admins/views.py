from django.http import JsonResponse
from django.shortcuts import render,redirect,HttpResponse
from django.views import View
from app02 import models
from admins.commom import auth_code
from admins.commom import common
# Create your views here.
def admins(request):
    return
class Login(View):
    def get(self,request,name):
        if name:
            request.session['IS_LOGIN'] = False
        return render(request, "login.html")
        pass
    def post(self,request,name):
        username: str = request.POST.get("username")
        password = request.POST.get("password")
        print(username, password)
        if username[0].isdigit():
            obj = models.User.objects.filter(height=username, password=password)
        else:
            obj = models.User.objects.filter(name=username, password=password)
        if obj:
            request.session['IS_LOGIN'] = True
            request.session["name"] = obj.first().name
            request.session["user_type"] = obj.first().user_type
            request.session.set_expiry(0)
            # return redirect("/show/")
            res = {"flag": 1, "msg": "登陆成功！"}
        else:
            res = {"flag": 0, "msg": "用户名或密码错误！"}
        return JsonResponse(res)

def get_yzm(request):
    auth_list = list(auth_code.auth_code())
    res={"str":auth_list[0].lower(),"path":auth_list[1]}
    print(res)
    return JsonResponse(res)

def register(request):
    if request.method == "GET":
        return render(request,"register.html")






