#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : MeUtils.
# @File         : wechat
# @Time         : 2021/6/7 11:17 上午
# @Author       : yuanjie
# @WeChat       : 313303303
# @Software     : PyCharm
# @Description  :

from meutils.pipe import *
from meutils.hash_utils import *


class Text(BaseConfig):
    content = ""


class Bot(object):

    def __init__(self, key='1eb25317-39a1-4af7-a6e3-63877ec2dd64'):
        self.hook_url = f'https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key={key}'

    def send(self, body=None):
        if body is None:
            body = {
                "msgtype": "text",
                "text": {
                    "content": "南京今日天气：29度，大部分多云，降雨概率：60%",
                    "mentioned_list": ["yuanjie", "@all"],
                    "mentioned_mobile_list": ["18550288233", "@all"]
                }
            }
        return requests.post(url=self.hook_url, json=body)

    def send_news(self):
        # json = {
        #     "msgtype": "news",
        #     "news": {
        #         "articles": [
        #             {
        #                 "title": "中秋节礼品领取",
        #                 "description": "今年中秋节公司有豪礼相送",
        #                 "url": "www.qq.com",
        #                 "picurl": "http://res.mail.qq.com/node/ww/wwopenmng/images/independent/doc/test_pic_msg1.png"
        #             }
        #         ]
        #     }
        # }
        pass

    def send_markdown(self):
        # json = {
        #     "msgtype": "markdown",
        #     "markdown": {
        #         "content": """
        #         实时新增用户反馈<font color="warning">132例</font>，请相关同事注意。\n
        #          >类型:<font color="comment">用户反馈</font>
        #          >普通用户反馈:<font color="comment">117例</font>
        #          >VIP用户反馈:<font color="comment">15例</font>
        #          """.strip(),
        #         "mentioned_list": ["wangqing", "@all"],  # 不支持艾特
        #     }
        # }
        pass

    def send_image(self, path):
        bytes_data = self.get_bytes(path)
        body = {
            "msgtype": "image",
            "image": {
                "base64": bytes2base64(bytes_data),
                "md5": md5(bytes_data, False)
            }
        }
        return self.send(body)

    def send_file(self, path, type='file'):
        upload_media_url = f'https://qyapi.weixin.qq.com/cgi-bin/webhook/upload_media?key={key}&type={type}'

        # bytes_data = self.get_bytes(path)
        # files = {'data': bytes_data} # 这样文件名为data

        with open(path, 'rb') as f:
            files = {'data': f}
            response = requests.post(upload_media_url, files=files)

        media_id = response.json()['media_id']

        body = {"msgtype": type, type: {"media_id": media_id}}
        return self.send(body)

    def get_bytes(self, path):
        if path.startswith('http'):
            bytes_data = requests.get(path).content
        else:
            bytes_data = Path(path).read_bytes()
        return bytes_data


if __name__ == '__main__':
    bot = Bot()
    # bot.send()
    # bot.send_image("https://www.baidu.com/img/flexible/logo/pc/result.png")

    bot.send_file('wechat.py')
