# coding=utf-8
# 调用旷视的官方美颜api 2021-04-04
# pip install requests
import base64
import requests
import json
import sys

import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
log = logging.getLogger(__name__)


def main(file='C://Users/zhangfan36/Desktop/简历/证件照.jpg'):
    # 准备好必要参数
    beautiful_url='https://api-cn.faceplusplus.com/facepp/v2/beautify'
    api_key='kTseH9TtSH_Hody8k15fhkRzyXpEuhmJ'
    api_secret='9kNy0Utc-mIDTtnvwVWuzHv3uQgIdscZ'
    with open(file,'rb') as f:
        image_base64=base64.b64encode(f.read())

    data={
        'api_key':api_key,
        'api_secret':api_secret,
        'image_base64':image_base64,
        'whitening':50, #美白
        'smoothing':50, #磨皮
        'thinface':50, #瘦脸
        'shrink_face':50, #小脸
        'enlarge_eye':50, #大眼
        'remove_eyebrow':50, #去眉毛
        #'filter_type':     #滤镜
    }

    r= requests.post(beautiful_url, data=data)
    html=json.loads(r.text)

    result=html['result']
    img_data=base64.b64decode(result)
    with open('D://证件照.jpg','wb') as f:
        f.write(img_data)
        log.info('文件生成完毕')
