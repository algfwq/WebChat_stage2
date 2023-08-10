from celery import shared_task
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from app.models import Settings, User
from django.core import mail
from PIL import Image, ImageDraw, ImageFont
import random
import os

# 配置日志记录器
import logging
logger = logging.getLogger('django')

# 异步发送验证邮件
@shared_task
def send_code(group_name,email_message,recipient_list):
    print("开始向" + str(recipient_list) + "发送验证码")
    channel_layer = get_channel_layer()  # 实例化get_channel_layer()对象，用于向组群发送消息
    #开始发送验证码
    try:
        mail.send_mail(
            subject='注册' + Settings.objects.get(id=1).web_name,  # 题目
            message=email_message,  # 消息内容
            from_email='algpythontest@outlook.com',  # 发送者[当前配置邮箱]
            recipient_list=recipient_list,  # 接收者邮件列表
            auth_password='ss699610'  # 在QQ邮箱->设置->帐户->“POP3/IMAP......服务” 里得到的在第三方登录QQ邮箱授权码
        )
        async_to_sync(channel_layer.group_send)(
            group_name,
            {
                "type": "email_code",
                'mode': 'code_message',
                'message': '验证码发送成功！'
            }
        )
    except:
        logger.error('邮件发送失败：' + str(recipient_list))
        async_to_sync(channel_layer.group_send)(
            group_name,
            {
                "type": "email_code",
                'mode': 'code_message',
                'message': '发送验证码出现异常！请检查你的邮箱！'
            }
        )

@shared_task
def create_image(username,text):
    def random_gradient_color():
        start_color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
        end_color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))

        # 创建一个新的图片，尺寸为200x200像素，白色背景
        image = Image.new('RGB', (200, 200))

        for y in range(200):
            r = start_color[0] + int((end_color[0] - start_color[0]) * y / 200)
            g = start_color[1] + int((end_color[1] - start_color[1]) * y / 200)
            b = start_color[2] + int((end_color[2] - start_color[2]) * y / 200)
            for x in range(200):
                image.putpixel((x, y), (r, g, b))

        return image

    # 生成包含两个字母的图片
    # 创建渐变背景色图片
    gradient_image = random_gradient_color()

    # 创建一个新的图片，尺寸为200x200像素
    image = Image.new('RGB', (200, 200))

    # 将渐变背景色图片合并到新图片中
    image.paste(gradient_image, (0, 0))

    draw = ImageDraw.Draw(image)

    # 获取当前文件路径
    current_path = os.path.abspath(__file__)
    font = ImageFont.truetype(os.path.abspath(os.path.dirname(current_path) + os.path.sep + ".") + '/ttf/1.ttf', 48)
    # 在中心位置绘制白色字母
    bbox = draw.textbbox((0, 0), text, font=font)

    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]

    x = (200 - text_width) / 2
    y = (200 - text_height) / 2
    draw.text((x, y), text, fill='white', font=ImageFont.truetype(os.path.abspath(os.path.dirname(current_path) + os.path.sep + ".") + '/ttf/1.ttf', 48))

    # 保存图片
    image.save(os.path.abspath(os.path.dirname(current_path) + os.path.sep + ".") + "/user_image/" + username + '.png')
