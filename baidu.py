from aip import AipSpeech
import requests
import random
import hashlib
import json

""" 你的 APPID AK SK """
APP_ID = '19802591'
API_KEY = 't8ApAnmbwm96VBgg0QCu1Njs'
SECRET_KEY = '1mbTXt2G2hyqLs0cbEtRVOG6IaDsqKpQ'

client = AipSpeech(APP_ID, API_KEY, SECRET_KEY)

trans_APP_ID='20200510000447331'
pwd='r0hdj_MZqXaW7s7SJWqD'
def translate(q,from_lang,to_lang):
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
        'sign':sign
    })

    return json.loads(r.text)['trans_result'][0]['dst']

if __name__ =="__main__":
    print(translate('你是傻子','zh','en'))