from xqyunpan import settings
import os
def auth_code():
    # 导入random模块
    import random
    # 导入Image,ImageDraw,ImageFont模块
    from PIL import Image, ImageDraw, ImageFont  ###这里需要安装pillow库 ，单独安装PIL可能无法安装
    # 定义使用Image类实例化一个长为120px,宽为30px,基于RGB的(255,255,255)随机颜色的画布（验证码图片背景）
    img1 = Image.new(mode="RGB", size=(120, 35), color=(random.randint(1,122), random.randint(1,122), random.randint(1,122)))
    # 实例化一支画笔
    draw1 = ImageDraw.Draw(img1, mode="RGB")

    L = []
    for i in range(5):
        # 每循环一次,从a-Z中随机生成一个字母或数字
        # 65到90为字母的ASCII码,使用chr把生成的ASCII码转换成字符

        x = random.randint(1,2)
        if x ==1:
            char1 = random.choice([chr(random.randint(65, 90)),chr(random.randint(97,122))])
        else:
            char1 = random.choice([chr(random.randint(48, 57))])
        L.append(char1)
        # 每循环一次重新生成随机颜色777
        color1 = (random.randint(122, 255), random.randint(122, 255), random.randint(122, 255))

        # 把生成的字母或数字添加到图片上
        # 图片长度为120px,要生成5个数字或字母则每添加一个,其位置就要向后移动24px
        # 定义要使用的字体
        # font1 = ImageFont.truetype("kumo.ttf", 28)
        # font1 = ImageFont.truetype("segoeui.ttf", random.randint(22,28))
        font1 = ImageFont.truetype("consola.ttf", random.randint(20,40))
        draw1.text([i * 24, 0], char1, color1, font=font1)

    # 把生成的图片保存为"pic.png"格式
    pic_path = "%s.jpeg"%str(random.randint(0,3)*10+random.randint(1,9))
    with open(os.path.join(settings.BASE_DIR,"static","login_pic",pic_path), "wb") as f:
        img1.save(f, format="jpeg")
    return "".join(L),os.path.join("static","login_pic",pic_path) # 返回验证码字符串和图片相对路径（这是我配置的我的项目路径，自己用的时候记得改打开文件路径）


