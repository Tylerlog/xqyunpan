# -*- coding: UTF-8 -*-
import os
import shutil


def copy_and_zip(file_dict, dst_folder_name):
    '''
    批量复制文件到指定文件夹，然后把指定文件夹的内容压缩成ZIP并且删掉该文件夹
    :param file_dict: 文件或文件夹
    :param dst_folder_name: 目标压缩文件的名称
    :return:
    '''
    source = os.path.join(os.getcwd(), dst_folder_name)
    if os.path.isfile(source + ".zip"):
        # print('aaa')
        os.remove(source + ".zip")  # 删除 dst_folder_name 文件，避免数据重复
    for key,values in file_dict.items():
        copy_file(key,values, dst_folder_name)

    # 这里我把输出文件的路径选到了程序根目录下

    # print(source)
    shutil.make_archive(source, "zip", source)
    shutil.rmtree(source)  # 删除
    return source+".zip"


def copy_file(new_name,srcfile, filename):
    '''
    把文件或文件夹复制到指定目录中
    :param srcfile: 文件或者文件夹的绝对路径
    :param filename: 指定目录
    :return:
    '''
    dstfile = os.path.abspath(os.getcwd())
    # 这里我把输出文件的路径选到了程序根目录下
    folder_name = dstfile + os.sep + filename + os.sep
    if not os.path.isfile(srcfile):
        last_name = os.path.basename(srcfile)
        destination_name = folder_name + last_name
        shutil.copytree(srcfile, destination_name)
        # print("copy %s -> %s" % (srcfile, destination_name))
    else:
        fpath, fname = os.path.split(folder_name)  # 分离文件名和路径
        if not os.path.exists(fpath):
            os.makedirs(fpath)  # 创建路径

        shutil.copy2(srcfile, folder_name+new_name)  # 移动文件
        # print("copy %s -> %s" % (srcfile, folder_name))


def ZIP(file_dict: dict, folder_name):
    folder_name = os.path.join('data', 'zip',folder_name)
    return copy_and_zip(file_dict, folder_name)


if __name__ == '__main__':
    # 压缩后文件路径到程序根目录下
    # file_list为字典，可以是多个文件或目录
    file_list = [r""]
    # ZIP(file_list, "dst_folder_name")  # 注意：这个压缩后的文件名不要随意更改，否则删除自身文件后自负！！
