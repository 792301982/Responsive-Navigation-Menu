from aip import AipSpeech
import requests
import random
import hashlib
import json
import uuid
import time
from googletrans import Translator

""" 你的 APPID AK SK """
APP_ID = '19802591'
API_KEY = 't8ApAnmbwm96VBgg0QCu1Njs'
SECRET_KEY = '1mbTXt2G2hyqLs0cbEtRVOG6IaDsqKpQ'

client = AipSpeech(APP_ID, API_KEY, SECRET_KEY)

def trans_baidu(q,from_lang,to_lang):
    trans_APP_ID='20200510000447331'
    pwd='r0hdj_MZqXaW7s7SJWqD'
    salt=str(random.randint(1,1000000))
    s=trans_APP_ID+q+salt+pwd
    sign=hashlib.md5(s.encode(encoding='UTF-8')).hexdigest()
    r=requests.post('http://api.fanyi.baidu.com/api/trans/vip/translate',
    data={
        'q':q,
        'from':from_lang,
        'to':to_lang,
        'appid':trans_APP_ID,
        'salt':salt,
        'sign':sign,
        
    })
    return json.loads(r.text)['trans_result'][0]['dst']

def encrypt(signStr):
    hash_algorithm = hashlib.sha256()
    hash_algorithm.update(signStr.encode('utf-8'))
    return hash_algorithm.hexdigest()

def truncate(q):
    if q is None:
        return None
    size = len(q)
    return q if size <= 20 else q[0:10] + str(size) + q[size - 10:size]

def trans_youdao(q,from_lang,to_lang):
    APP_KEY='108b5b19fdd6193f'
    APP_SECRET='005cpn1658bpIPpkDt0oaKsjq11CVpw9'
    salt=str(uuid.uuid1())
    curtime = str(int(time.time()))
    s=APP_KEY + truncate(q) + salt + curtime + APP_SECRET
    sign=encrypt(s)
    r=requests.post('https://openapi.youdao.com/api',
    data={
        'q':q,
        'from':from_lang,
        'to':to_lang,
        'appKey':APP_KEY,
        'salt':salt,
        'sign':sign,
        'signType':'v3',
        'curtime':curtime
    })
    print(r.text)
    return ''.join(json.loads(r.text)['translation'])

def trans_google(q,from_lang,to_lang):
    translator = Translator(service_urls=['translate.google.cn'])
    text = translator.translate(q,src=from_lang,dest=to_lang).text
    return text

if __name__ =="__main__":
    print(trans_google('你是傻子','zh-cn','en'))