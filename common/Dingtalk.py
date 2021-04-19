# -*- coding: utf-8 -*-

import requests
import json
import time
import hmac
import hashlib
import base64
import urllib.parse

timestamp = str(round(time.time() * 1000))
secret = 'SEC19b87a3d40c146786c83229cccc58175a038bcb5480bd52363d4416ccb2b89c0'
secret_enc = secret.encode('utf-8')
string_to_sign = '%s\n%s' % (timestamp, secret)
string_to_sign_enc = string_to_sign.encode('utf-8')
hmac_code = hmac.new(secret_enc, string_to_sign_enc, digestmod=hashlib.sha256).digest()
sign = urllib.parse.quote_plus(base64.b64encode(hmac_code))


def send_text_ding(content: str, dk_url: str):
    """
    封装钉钉text格式群发消息
    用例钉钉的第三方的api，发送成功是返回True 失败返回False
    """
    try:
        dk_url = dk_url + '&timestamp=%s&sign=%s' % (timestamp, sign)
        data = {
            "msgtype": "text",
            "text": {
                "content": content
            },
            "isAtAll": True
        }
        headers = {
            'Content-Type': 'application/json'
        }
        f = requests.post(url=dk_url, data=json.dumps(data), headers=headers)
        if f.json()['errcode'] == 0:
            return True
        else:
            return False
    except:
        return False


def send_link_ding(text: str, title: str, dk_url: str, link: str):
    """
    封装钉钉text格式群发消息
    用例钉钉的第三方的api，发送成功是返回True 失败返回False
    """
    try:
        dk_url = dk_url + '&timestamp=%s&sign=%s' % (timestamp, sign)
        data = {
            "msgtype": "link",
            "link": {
                "text": text,
                "title": title,
                "picUrl": "",
                "messageUrl": link
            }
        }
        headers = {
            'Content-Type': 'application/json'
        }
        f = requests.post(url=dk_url, data=json.dumps(data), headers=headers)
        if f.json()['errcode'] == 0:
            return True
        else:
            return False
    except:
        return False


if __name__ == '__main__':
    access_token = '0fa5b764669ac07c1ccb1eb878249fdb4d701002a13b0a8c03b5d13f5e0ef11b'
    url = 'https://oapi.dingtalk.com/robot/send?access_token=%s' % access_token
    content = '这是一个python发送的测试消息b'
    send_text = send_text_ding(content, url)
    print(send_text)
    # text = '这是一个python发送的测试消息c'
    # title = '测试title c'
    # link = 'http://www.baidu.com'
    # send_link = send_link_ding(text, title, url, link)
    # print(send_link)
