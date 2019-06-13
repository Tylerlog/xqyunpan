from django.http import JsonResponse
from django.shortcuts import render,redirect,HttpResponse
from django.views import View
from app02 import models
from admins.commom import auth_code
from admins.commom import common
from django.db import transaction
import re
# Create your views here.
def admins(request):
    return
class Login(View):
    def get(self,request,name):
        if name:
            request.session['login'] = False
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
            request.session['login'] = True
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
    else:
        username = request.POST.get("username")
        password = request.POST.get("password")
        cellphone = request.POST.get("cellphone")
        if len(password) < 3:
            res = {"flag": 0, "msg": "密码长度不合法！"}
        elif not username[0].isalpha():
            res = {"flag": 0, "msg": "用户名必须以字母开头！"}
        else:
            flag = False
            with transaction.atomic():
                userinfo_obj = models.UserInfo.objects.create(cellphone=cellphone)
                user_obj = models.User.objects.create(name=username,password=password,userinfo=userinfo_obj,user_type="user")
                flag = True
            if flag:
                res = {"flag":1,"msg":"恭喜你！，注册成功！"}
            else:
                res = {"flag": 0, "msg": "注册失败！"}
        return JsonResponse(res)


def textname(request):
    if request.method == "GET":
        return render(request,"error.html")
    elif request.method == "POST":
        if request.POST.get("type") == "phone":
            user_obj = models.UserInfo.objects.filter(cellphone=request.POST.get("cellphone"))
            if user_obj:
                res = {"flag":0,"msg":"当前手机号已注册！"}
            else:
                res = {"flag":1,"msg":""}
            print(user_obj)
        elif request.POST.get("type") == "name":
            if (request.POST.get("username")):
                if (request.POST.get("username"))[0].isdigit():
                    res = {"result":0,"msg":"用户名不能以数字开头！"}
                elif len(request.POST.get("username"))<3:
                    res = {"result":0,"msg":"用户名必须不少于3位！"}
                elif request.POST.get("username"):
                    if models.User.objects.filter(name=request.POST.get("username")):
                        res = {"result":0,"msg":"很遗憾！该用户名已被占用！"}
                    else:
                        res = {"result":1,"msg":"恭喜你！可以注册！"}
                else:
                    res = {"result":1,"msg":""}
            else:
                res = {"result":1,"msg":""}
        return JsonResponse(res)

def get_cell_yzm(request):
    if request.method == "POST":
        phone = request.POST.get("cell")
        regexp = "^((13[0-9])|(15[^4])|(18[0,2,3,5-9])|(17[0-8])|(147))\\d{8}$"
        str_list = re.findall(regexp, phone)
        if not str_list:
            res = {"flag": 0, "msg": "手机号不合法！请重新输入！"}
        else:
            num_str = common.create_yzm()
            print('123',num_str)
            result = common.msm(phone,num_str)
            res = {"flag":1,"phone":phone,"yzm":num_str}
        return JsonResponse(res)
    else:return render(request,"error.html")

def changeinfo(request):
    if request.method == "GET":
        user = {}
        user_obj = models.User.objects.filter(id = request.GET.get("id")).first()
        user["id"] = user_obj.id
        user["name"] = user_obj.name
        user["user_type"] = user_obj.user_type
        user["picture_path"] = user_obj.picture_path
        user["gender"] = user_obj.userinfo.gender
        user["cellphone"] = user_obj.userinfo.cellphone
        user["birthday"] = user_obj.userinfo.birthday.isoformat()
        user["info"] = user_obj.userinfo.info
        print(user)
        return render(request, "myinfo.html", locals())
    else:
        print(request.POST)
        id = request.POST.get("id")
        user_obj = models.User.objects.filter(id=id).first()
        if request.POST.get("password"):
            user_obj.password = request.POST.get("password")
        if request.POST.get("cellphone"):
            user_obj.userinfo.cellphone = request.POST.get("cellphone")
        user_obj.userinfo.birthday = request.POST.get("birthday")
        user_obj.userinfo.gender = request.POST.get("gender")
        if request.POST.get("info"):
            user_obj.userinfo.info = request.POST.get("info")
        user_obj.save()
        user_obj.userinfo.save()
        return redirect("/admins/myinfo/")



        # if


        # return render(request,"home.html")

        # user_id = request.POST.get("user_id")
        # new_password = request.POST.get("new_password")
        # gender = request.POST.get("gender")
        # cellphone = request.POST.get("new_cellphone")
        # user_info = request.POST.get("user_info")
        # birthday = request.POST.get("birthday")



