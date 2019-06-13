# 实现方式 MD5(path,split_num=10)
def file_md5(path: str, split_num=256, get_byte=8):
    """
    把文件路径传入，按需求分割，返回一个MD5加密序号
    :param path: 传入文件路径
    :param split_num: 需要分割生成MD5的数量，默认8
    :get_byte: 每段需要取的字节个数，默认256字节
    大小为2MB的文件直接MD5
    """
    import os
    import hashlib
    # 判断 split_num和get_byte 是否为数字
    if not isinstance(split_num, int) or split_num <= 0:
        raise TypeError("split_num 必须为不为0的正整数")
    if not isinstance(get_byte, int) or get_byte <= 0:
        raise TypeError("get_byte 必须为不为0的正整数")

    # 判断path是否为文件
    if not os.path.isfile(path):
        raise TypeError("%s 不存在该文件！" % path)

    size = os.path.getsize(path)
    if size < split_num * get_byte:
        # 读出文件
        with open(path, 'rb') as f1:
            f1 = f1.read()
        # 进行加密
        cipher = hashlib.md5()
        cipher.update(str(split_num).encode('utf-8'))
        cipher.update(f1)
        cipher.update(str(get_byte).encode('utf-8'))
        return cipher.hexdigest()
    # 每段分的大小
    mean_size = size // split_num
    cipher = hashlib.md5()
    # 位置
    place = 0
    with open(path, 'rb') as f1:
        for i in range(split_num):
            f1.seek(place)
            res = f1.read(get_byte)
            cipher.update(res)
            place = place + mean_size

    return cipher.hexdigest()

if __name__ == '__main__':
    # 使用方法
    print(file_md5(r'F:\aaa.mp4'))
