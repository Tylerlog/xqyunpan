import hashlib
import json
import os
import random
from datetime import *

from django.db.models import Q
from django.http import Http404, FileResponse
from django.http import JsonResponse
from django.shortcuts import render,redirect

from app02.models import User, File, File_Users, Share
from app02.py import zip
from admins.commom import common

# Create your views here.

@common.is_login
def home(request):
    return redirect('/home/all')


# 所有文件
@common.is_login
def all(request):
    if request.session.get("login"):
        user_info = {"id": request.session.get("id"),'img':request.session.get("img"),'name':request.session.get("name")}
        print(user_info)
        return render(request, 'home.html',locals())

    else:
        return render(request, "login.html")



# 图片文件
@common.is_login
def pic(request):
    if request.session.get("login"):
        user_info = {"id": request.session.get("img"),'img':request.session.get("img"),'name':request.session.get("name")}
        print(user_info)
        return render(request, 'pic.html',locals())

    else:
        return render(request, "login.html")


# 文档文件
@common.is_login
def doc(request):
    if request.session.get("login"):
        user_info = {"id": request.session.get("img"),'img':request.session.get("img"),'name':request.session.get("name")}
        print(user_info)
        return render(request, 'doc.html',locals())

    else:
        return render(request, "login.html")


# 视频文件
@common.is_login
def video(request):
    if request.session.get("login"):
        user_info = {"id": request.session.get("img"),'img':request.session.get("img"),'name':request.session.get("name")}
        print(user_info)
        return render(request, 'video.html',locals())

    else:
        return render(request, "login.html")


# 音乐文件
@common.is_login
def music(request):
    if request.session.get("login"):
        user_info = {"id": request.session.get("img"),'img':request.session.get("img"),'name':request.session.get("name")}
        print(user_info)
        return render(request, 'music.html',locals())

    else:
        return render(request, "login.html")


# 其他文件
@common.is_login
def rests(request):
    if request.session.get("login"):
        user_info = {"id": request.session.get("img"),'img':request.session.get("img"),'name':request.session.get("name")}
        print(user_info)
        return render(request, 'rests.html',locals())

    else:
        return render(request, "login.html")


# 分享中心
@common.is_login
def share(request):
    if request.session.get("login"):
        user_info = {"id": request.session.get("img"),'img':request.session.get("img"),'name':request.session.get("name")}
        print(user_info)
        return render(request, 'share.html',locals())

    else:
        return render(request, "login.html")


def aaa(request):
    return render(request, 'aaa.html')


# 进行加密文件夹
def file_md5_name(file, time=None):
    res = gain_time
    cipher = hashlib.md5()
    if time:
        cipher.update(str(time).encode('utf-8'))
    cipher.update(str(res).encode('utf-8'))
    cipher.update(file.encode('utf-8'))
    res = cipher.hexdigest()
    return res


# 上传文件
@common.is_login
def upload(request):
    # 需要一个登陆的用户名字
    user = request.session.get("name")
    # 需要一个file_path
    file_path = 'c:'

    file_obj = request.FILES.get('file')
    file_name = file_obj.name  # 文件名

    # 首先获取文件名字，看用户的同文件夹中是否有同名文件
    name_id = request.session.get("id")  # 获取操作用户的ID

    # 获取文件名字
    get_file_name = File_Users.objects.filter(
        Q(user_id=name_id) , ~Q(file_path=file_path) , Q(file_name=file_name)).first()

    # 如果文件名字已存在就返回已存在
    if get_file_name:
        return JsonResponse({'code': 1, 'file_name': file_name})

    # ---------------------------文件无重名，继续-------------------------------------------

    # 判断系统后台是否有此文件，有就可以实现秒传重指向

    res = request.POST.get('md5')  # 转码校验，获取前端发送来的MD5校验
    # 判断系统后台是否有此文件
    res = json.loads(res)
    res = res.get(file_name)
    file_data = File.objects.filter(data=res).first()
    if file_data:
        # 用户的ID：name_id
        # 用户文件名字： file_name
        # 用户文件的路径：file_path

        # 文件的ID
        file_id = file_data.id
        tag, stamp = save(file_id, name_id, file_name, file_path)
        if tag:

            return JsonResponse({'code': 2, 'file_name': file_name}, )
        else:
            return JsonResponse({'code': 3, 'file_name': file_name})
    else:
        # 存放服务器文件路径
        path = os.path.join(os.getcwd(), 'data')
        # 如果服务器没有此文件夹就创建
        if not os.path.exists(path):
            os.makedirs(path)
        # 存放服务器文件名
        file_data_name = os.path.join(path, file_md5_name(file_name))  #

        # 如果文件名已存在就修改名字

        # 存入服务器真实文件
        with open(file_data_name, 'wb') as f:
            for i in file_obj:
                f.write(i)
        # 存入数据
        # 存入真实文件地址

        size = bytes2human(os.path.getsize(file_data_name))  # 转换文件大小
        get_file_type = file_type(file_obj.name)  # 得到文件的类型
        # 存入文件的数据库中
        File.objects.create(path=file_data_name, data=res, size=size, type=get_file_type)
        # 存入多对多关联表

        file_id = File.objects.filter(data=res).first().id
        # 存入用户表
        tag, stamp = save(file_id, name_id, file_name, file_path)
        if tag:

            return JsonResponse({'code': 0, 'file_name': file_name})
        else:
            return JsonResponse({'code': 3, 'file_name': file_name})


# 获取当前时间
def gain_time():

    tim = (datetime.now()+ timedelta(hours=8)).strftime('%Y-%m-%d %H:%M:%S')  # 当前时间
    return tim


# 生成文件大小的符合的
def bytes2human(n):
    """
    >>> bytes2human(10000)
    9K
    >>> bytes2human(100001221)
    95M
    """
    symbols = ('K', 'M', 'G', 'T', 'P', 'E', 'Z', 'Y')
    prefix = {}
    for i, s in enumerate(symbols):
        prefix[s] = 1 << (i + 1) * 10

    for s in reversed(symbols):
        if n >= prefix[s]:
            value = int(float(n) / prefix[s])
            return '%s%s' % (value, s)
    return '%sB' % n


# p判断文件类型
def file_type(file_name: str):
    name = file_name.split('.')[-1].upper()
    # 判断是否为图片
    if name in ['JPG', 'Webp', 'BMP', 'PCX', 'TIF', 'GIF', 'JPEG', 'TGA', 'JPG',
                'EXIF', 'FPX', 'SVG', 'PSD', 'CDR', 'PCD', 'DXF', 'UFO', 'EPS',
                'AI', 'PNG', 'HDRI', 'RAW', 'WMF', 'FLIC', 'EMF', 'ICO']:
        return '图片'
    # 判断是否为文档
    elif name in ['JAVA', 'XML', 'JSON', 'CONF', 'JSP', 'PHPS', 'ASP', 'PROJECT',
                  'CLASSPATH', 'SVN', 'GITIGNORE', 'TXT', 'LOG', 'SYS', 'INI', 'PDF',
                  'XLS', 'XLSX', 'DOC', 'PPT', 'EXE', 'MSI', 'BAT', 'SH', 'RPM', 'DEB',
                  'BIN', 'DMG', 'PKG', 'CLASS', 'DLL', 'SO', 'A', 'KO', 'RAR', 'ZIP',
                  'ARJ', 'GZ', 'TAR', 'TAR.GZ', '7Z', 'HTM', 'HTML', 'JS', 'CSS', 'MD']:
        return '文档'
    # 判断是否为视频MP3、WMA、AVI、RM、RMVB、FLV、MPG、MOV、MKV
    elif name in ['MP4', 'M4V', 'MOV', 'QT', 'AVI', 'FLV', 'WMV',
                  'ASF', 'MPEG', 'MPG', 'VOB', 'MKV', 'ASF', 'RM', 'FLV', 'AVI',
                  'VOB', 'DAT']:
        return '视频'
    elif name in ['MP3', 'WMA', 'APE', 'FLAC', 'AAC', 'AC3', 'MMF', 'AMR', 'M4A', 'M4R', 'WAV', 'MP2']:
        return '音乐'
    else:
        return '其他'


# 用户数据进行存储
def save(file_id, user_id, file_name, file_path):
    try:
        time = gain_time()

        File_Users.objects.create(time=time, user_id=user_id, File_id=file_id, file_name=file_name, file_path=file_path)
        return True, '秒传成功！'
    except Exception as a:
        return False, a


# 查询文件列表
@common.is_login
def select(request):
    user = request.session.get("name")
    # 获取用户的ID
    user_id = request.session.get("id")
    # table返回信息
    info = {"code": 200, "msg": "", "count": 100, "data": []}

    # 文件类型
    func = {'all': '', 'pic': '图片', 'doc': '文档', 'video': '视频', 'music': '音乐', 'rests': '其他'}
    if request.method == 'POST':

        type = request.POST.get('type')
        if type in func:
            page = int(request.POST.get('page'))  # 第几页
            limit = int(request.POST.get('limit'))  # 每页数量
            filename = request.POST.get('filename')
            data = File_Users.objects.filter(Q(file_name__icontains=filename)
                                             , Q(File__type__icontains=func[type]), user_id=user_id)
        else:
            return JsonResponse(info)
    else:

        type = request.GET.get('type')
        if type in func:
            # 获取所有的数据
            page = int(request.GET.get('page'))  # 第几页
            limit = int(request.GET.get('limit'))  # 每页数量
            data = File_Users.objects.filter(Q(File__type__icontains=func[type]), user_id=user_id)
        else:
            return JsonResponse(info)

    x = 0
    # 设置图标
    file_font = {"文件夹": "fa-folder", "图片": "fa-file-image-o", "文档": "fa-file-text", "视频": "fa-file-movie-o",
                 "音乐": "fa-file-sound-o", "其他": "fa-file"}

    for i in data:

        # obj = File.objects.filter(id=file_id).first()
        x += 1

        if x <= (page * limit) and x > ((page - 1) * limit):
            a = {
                "id": x,
                "t_id": i.id,
                "filename": i.file_name,
                "ope": i.File.data,
                "size": i.File.size,
                "datetime": i.time,
                "experience": i.File.type,
                "type": file_font[i.File.type]
            }
            info["data"].append(a)
    info["count"] = x
    return JsonResponse(info)


# 查找需要下载的文件路径
def download_file(file_id):
    obj = File_Users.objects.filter(id=file_id).first()
    obj_path = obj.File.path
    return obj_path
    pass


# 文件下载
def download(request, data):
    # 分割名字和文件校验数据

    dow_data, dow_name = data.split('/')
    # 查询文件在服务器的路径
    file_path = File.objects.filter(data=dow_data).first().path

    ext = os.path.basename(file_path).split('.')[-1].lower()
    # 不让客户下载的文件路径
    if ext not in ['py', 'db', 'sqlite3']:
        response = FileResponse(open(file_path, 'rb'))
        response['content_type'] = "application/octet-stream"
        response['Content-Disposition'] = 'attachment; filename=' + dow_name
        return response
    else:
        raise Http404


# 下载多个文件
def download_pack(request):
    if request.method == 'POST':
        info = {}
        data = json.loads(request.POST.get('data')).get('data')
        # 获取文件所在服务器的路径，用列表info接
        sum = 0
        for i in data:
            sum += 1
            res = File_Users.objects.filter(id=i.get('t_id')).first()
            if res:
                info[i.get('filename')] = (res.File.path)

        # 文件打包
        dow_name = file_md5_name(str(info), gain_time())

        res_path = zip.ZIP(info, dow_name)
        new_path = os.path.join(os.getcwd(), 'data', dow_name)
        with open(res_path, 'rb') as f1, \
                open(new_path, 'wb') as f2:
            f2.write(f1.read())
            os.remove(res_path)

        # 拼接返回下载路径
        file_path = os.path.join('/home/','download', dow_name, '%s-number-file' % sum + '.zip')
        # 存入数据库
        File.objects.create(path=new_path, data=dow_name, size=0, type='zip')
        return JsonResponse({'start': 1, 'msg': '正在下载。。', 'file_path': file_path, 'type': request.POST.get('type')})
    return JsonResponse({'start': 0, 'msg': '请求不合法'})


# 文件删除
@common.is_login
def delete(request):  # 提交过来删除有两种方式，一种是单个删除，一种是多个删除
    # 反 json 序列化，并get取值
    data = request.POST.get('data')
    if data:
        data = json.loads(request.POST.get('data')).get('data')
        for i in data:
            File_Users.objects.filter(id=i.get('t_id')).delete()
        return JsonResponse({'start': 1, 'msg': '删除成功！'})

    if request.method == 'POST':
        file_id = request.POST.get('file_id')
        if file_id:
            File_Users.objects.filter(id=file_id).delete()
            return JsonResponse({'start': 1, 'msg': '删除成功！'})

    return JsonResponse({'start': 0, 'msg': '非法访问！'})


# 文件修改
@common.is_login
def update(request):
    if request.method == 'POST':
        file_id = request.POST.get('file_id')
        if file_id:
            file_name = request.POST.get('file_name')
            File_Users.objects.filter(id=file_id).update(file_name=file_name)
            return JsonResponse({'start': 1, 'msg': '修改成功！'})

    return JsonResponse({'start': 0, 'msg': '非法访问！'})


def random_link(sum=10):
    code = ''
    for i in range(sum):
        add = random.choice([random.randrange(10), chr(random.randrange(65, 91))])
        code += str(add)
    return code


# 生成文件分享
@common.is_login
def share_page(request, data):
    # 需要一个用户名

    name = request.session.get("name")

    if request.method == 'POST':
        info = {}
        data = json.loads(request.POST.get('data')).get('data')
        # 获取文件所在服务器的路径，用列表info接
        sum = 0
        # 生成分享用户id
        user_id = User.objects.filter(name=name).first().id

        sum = len(data)
        # 生成分享名
        share_name = '%s分享%s的等%s个文件' % (name, data[0].get('filename'), sum)
        # 生成随机登录码
        code = random_link(10)
        # 生成随机密码
        password = random_link(4)

        # 存入share表
        Share_obj = Share.objects.create(share_name=share_name, share_password=password, share_path=code
                                         , user_id=user_id, share_time=gain_time())
        # 分享的文件表关联
        for i in data:
            File_Users_obj = File_Users.objects.filter(id=i.get('t_id')).first()
            Share_obj.File_Users.add(File_Users_obj)

        return JsonResponse({'start': 1, 'msg': share_name, 'file_path':request.POST.get('link') + code, 'password': password})
    return JsonResponse({'start': 0, 'msg': '请求不合法'})


# 查询分享文件列表
@common.is_login
def share_list(request):
    user = request.session.get("name")
    # 获取用户的ID
    user_id = request.session.get("id")
    # table返回信息
    info = {"code": 200, "msg": "", "count": 100, "data": []}

    post_type = request.POST.get('type')
    get_type = request.GET.get('type')
    if post_type == 'share' or get_type == 'share':
        if request.method == 'POST':
            link = request.POST.get('link')
            page = int(request.POST.get('page'))  # 第几页
            limit = int(request.POST.get('limit'))  # 每页数量
            filename = request.POST.get('filename')
            data = Share.objects.filter(Q(share_name__icontains=filename), user_id=user_id)
        else:

            link = request.GET.get('link')

            # 获取所有的数据
            page = int(request.GET.get('page'))  # 第几页
            limit = int(request.GET.get('limit'))  # 每页数量
            data = Share.objects.filter(user_id=user_id)
    else:
        return JsonResponse(info)

    x = 0
    # 设置图标
    for i in data:
        x += 1

        if x <= (page * limit) and x > ((page - 1) * limit):
            a = {
                "id": x,
                "t_id": i.id,
                "share_name": i.share_name,
                "ope": "",
                "share_path": link + i.share_path,
                "share_password": i.share_password,
                "share_time": i.share_time,

            }
            info["data"].append(a)
    info["count"] = x
    return JsonResponse(info)


# 文件删除
@common.is_login
def share_cancel(request):  # 提交过来删除有两种方式，一种是单个删除，一种是多个删除
    # 反 json 序列化，并get取值
    data = request.POST.get('data')
    if data:
        data = json.loads(request.POST.get('data')).get('data')
        for i in data:
            Share.objects.filter(id=i.get('t_id')).delete()
        return JsonResponse({'start': 1, 'msg': '取消分享成功！'})

    if request.method == 'POST':
        file_id = request.POST.get('file_id')
        if file_id:
            Share.objects.filter(id=file_id).delete()
            return JsonResponse({'start': 1, 'msg': '取消分享成功！'})

    return JsonResponse({'start': 0, 'msg': '非法访问！'})

# 访客用户分享文件列表
def select_share_link(request,data):
    # table返回信息
    info = {"code": 200, "msg": "",'start': 0, "count": 100, "data": [],}
    # 获取密码和分享路径
    share_password = request.GET.get('password')
    if not share_password:
        share_password = request.POST.get('password')
    share_path = data.split('/')[-1]

    # 判断密码，如果为空，返回提示输入分享密码
    if share_password == '' or share_password==None:
        info['msg']='请输入分享密码！'
        return JsonResponse(info)

    # 获取分享路径
    # 判断密码是否一致
    share_obj = Share.objects.filter(share_path=share_path,share_password=share_password.upper()).first()
    # 如果校验错误，返回提示分享密码错误
    if not share_obj:
        info['msg'] = '分享密码错误！'
        return JsonResponse(info)


    # data.count()  获取数据个数
    # # 文件类型
    if request.method == 'POST':
        filename = request.POST.get('filename')
        page = int(request.POST.get('page'))  # 第几页
        limit = int(request.POST.get('limit'))  # 每页数量
        data_obj = Share.objects.filter(Q(share_name__icontains=filename),share_path=share_path
                                        ,share_password=share_password).first()
        if data_obj == None:
            data=[]
        else:
            data = data_obj.File_Users.all()
    else:

        # 获取所有的数据
        page = int(request.GET.get('page'))  # 第几页
        limit = int(request.GET.get('limit'))  # 每页数量
        data = share_obj.File_Users.all()

    x = 0
    # 设置图标
    file_font = {"文件夹": "fa-folder", "图片": "fa-file-image-o", "文档": "fa-file-text", "视频": "fa-file-movie-o",
                 "音乐": "fa-file-sound-o", "其他": "fa-file"}
    # 循环取值
    for i in data:
        x += 1
        if x <= (page * limit) and x > ((page - 1) * limit):
            a = {
                "id": x,
                "t_id": i.id,
                "filename": i.file_name,
                "ope": i.File.data,
                "size": i.File.size,
                "datetime": i.time,
                "experience": i.File.type,
                "type": file_font[i.File.type]
            }
            info["data"].append(a)
    info["count"] = x
    info["start"] = 1
    info["msg"] = '校验成功！'
    return JsonResponse(info)




def share_link(request,urls):
    # 首先校验分享网址是否存在
    share_obj = Share.objects.filter(share_path=urls)
    # 如果不存在，跳转错误页面
    if not share_obj:
        return render(request, 'error.html')

    return render(request, 'sharelink.html')


def title(request):
    return render(request,'pop-up.html')