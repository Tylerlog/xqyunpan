from django.db import models

# Create your models here.

class User(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=32) # 用户姓名
    password = models.CharField(max_length=32) # 用户密码
    cellphone = models.CharField(max_length=32) # 手机号
    user_type = models.CharField(max_length=32) # 用户类型
    register_time = models.DateField(auto_now_add=True) # 用户注册时间

class File(models.Model):

    path = models.CharField(max_length=200) # 文件的真实路径
    data = models.CharField(max_length=64) # 文件的校验数据
    size = models.CharField(max_length=64) # 文件是大小
    type = models.CharField(max_length=64) # 文件的类型

class File_Users(models.Model):
    user = models.ForeignKey(to='User') # 用户ID
    File = models.ForeignKey(to='File') # 文件ID
    file_name= models.CharField(max_length=200) # 文件的虚拟名字
    file_path= models.CharField(max_length=200) # 文件的虚拟路径
    time = models.CharField(max_length=64) # 客户自己文件的修改时间

class Share(models.Model):
    share_name = models.CharField(max_length=2000)  # 分享名
    share_password = models.CharField(max_length=64)  # 分享密码
    share_path = models.CharField(max_length=200)  # 分享访问路径===>>> 随机登录码
    user = models.ForeignKey(to='User')  # 分享的用户id
    share_time = models.CharField(max_length=64)  # 分享日期
    File_Users = models.ManyToManyField(to='File_Users')  # 分享表和文件表多对多


