
def isFloat(x):
    try:
        float(x)
        if str(x) in ['inf', 'infinity', 'INF', 'INFINITY', 'True', 'NAN', 'nan', 'False', '-inf', '-INF', '-INFINITY', '-infinity', 'NaN', 'Nan']:
            return False
        else:
            return True
    except:
        return False

import random
def create_yzm():
    return "".join([str(random.randint(0,9)) for i in range(6)])


# 验证码  调用格式 MSM("手机号",'用户名','验证码')
def msm(phone, number):
    from qcloudsms_py import SmsSingleSender
    from qcloudsms_py.httpclient import HTTPError
    # 短信应用SDK AppID
    appid = 1400217900  # SDK AppID是1400开头
    # 短信应用SDK AppKey
    appkey = "fe04cc0b081ba3037ef32c8093feeaf5"
    # 需要发送短信的手机号码
    phone_numbers = [phone]
    # 短信模板ID，需要在短信应用中申请
    template_id = 349381  #
    # 尊敬的用户，欢迎成为希希大队长社区用户！您的验证码是{1}，请于5分钟内填写。如非本人操作，请忽略本短信。

    # 签名
    sms_type = 0
    sms_sign = "希希大队长社区"
    ssender = SmsSingleSender(appid, appkey)
    params = [number
              ]  # 当模板没有参数时，`params = []`，数组具体的元素个数和模板中变量个数必须一致，例如事例中templateId:5678对应一个变量，参数数组中元素个数也必须是一个
    try:
        result = ssender.send_with_param(86, phone_numbers[0],
                                     template_id, params, sign=sms_sign, extend="",
                                     ext="")  # 签名参数未提供或者为空时，会使用默认签名发送短信
    except BaseException as e:
        return False
    return True

