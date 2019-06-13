from django.http import JsonResponse
from django.shortcuts import render,reverse

# Create your views here.
info = ""
choice = ""
code = ""  # ZpeVbzPOOwfakm51Evw7zT7XBMmoCXtS


def login(request):
    return render(request, 'login.html')

def aaa(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        password = request.POST.get('password')
        if name == 'qwe' and password=='123':
            return JsonResponse({'start':1,'msg':'登录成功！'})
        return JsonResponse({'start':0,'msg':'登录失败！'})
    return render(request, 'aaa.html')


def verify(request):
    result = request.POST.get("result")[-32:]
    global choice
    if choice:
        if result == choice:
            global info
            info = "stop"
            return JsonResponse({'status': 0, 'msg': '扫码成功！', 'md5': result})

    return JsonResponse({'status': 1, 'msg': '扫码网页不存在！', 'md5': ""})


def accredit(request):
    avatarUrl = request.POST.get("avatarUrl")  # 头像网址
    nickName = request.POST.get("nickName")  # 微信名
    gender = request.POST.get("gender")  # 姓名，1 男
    province = request.POST.get("province")  # 省
    city = request.POST.get("city")  # 城市
    country = request.POST.get("country")  # 国家
    code = request.POST.get("code")  # id
    md5 = request.POST.get("md5")  # 返回的md5

    global choice
    if choice:
        if md5 == choice:
            global info

            choice = ""
            if code:
                res = appid(code)['openid']
                win(request)
                return JsonResponse({'status': 0, 'msg': '登录成功！'})

def win(request):
    return render(request, 'error.html')
# 获取用户的唯一id
def appid(code):
    import requests
    APPID = 'wxe34fb04da7071b5b'
    SECRET = '9d7bb8620e49e96a2d72dc4034f183f3'
    JSCODE = code
    res = r"https://api.weixin.qq.com/sns/jscode2session?appid=" + APPID + "&secret=" + SECRET + "&js_code=" + JSCODE + "&grant_type=authorization_code"
    r = requests.get(url=res)
    import json
    top = json.loads(r._content.decode('utf-8'))
    return dict(top)


def random(request):
    res = request.POST.get("random")
    global info, choice
    choice = res
    tab = info
    info = ""
    return JsonResponse({'status': tab})


def error(request):
    return render(request, 'error.html')
    pass

