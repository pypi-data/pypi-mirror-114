#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : MeUtils.
# @File         : wechat
# @Time         : 2021/6/7 11:17 上午
# @Author       : yuanjie
# @WeChat       : 313303303
# @Software     : PyCharm
# @Description  :
from enum import Enum
import requests

from meutils.pipe import *


class Text(BaseConfig):
    content = ""




json = {
    "msgtype": "text",
    "text": {
        "content": "广州今日天气：29度，大部分多云，降雨概率：60%",
        "mentioned_list": ["wangqing", "@all"],
        "mentioned_mobile_list": ["13800001111", "@all"]
    }
}

json = {
    "msgtype": "news",
    "news": {
        "articles": [
            {
                "title": "中秋节礼品领取",
                "description": "今年中秋节公司有豪礼相送",
                "url": "www.qq.com",
                "picurl": "http://res.mail.qq.com/node/ww/wwopenmng/images/independent/doc/test_pic_msg1.png"
            }
        ]
    }
}

json = {
    "msgtype": "markdown",
    "markdown": {
        "content": """
        实时新增用户反馈<font color="warning">132例</font>，请相关同事注意。\n
         >类型:<font color="comment">用户反馈</font>
         >普通用户反馈:<font color="comment">117例</font>
         >VIP用户反馈:<font color="comment">15例</font>
         """.strip(),
        "mentioned_list": ["wangqing", "@all"],  # 不支持艾特
    }
}

json = {
    "msgtype": "image",
    "image": {
        "base64": "DATA",
        "md5": "MD5"
    }
}


if __name__ == '__main__':
    url = 'https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=a60788eb-9543-4bda-b857-906f832267d0'
    requests.post(url, json=json)
