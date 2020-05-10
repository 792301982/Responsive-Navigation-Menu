from flask import Flask, render_template, request
import os
import uuid
import translate
import json

app = Flask(
    __name__,
    static_folder='images',
)


@app.route('/')
def main():
    return render_template('index.html')

# 读取文件


def get_file_content(filePath):
    with open(filePath, 'rb') as fp:
        return fp.read()


@app.route('/getaudio', methods=['POST'])
def getaudio():
    audiofile = request.files.get("audioData")
    if audiofile:
        filepath = "audio/%s.pcm" % uuid.uuid4()
        audiofile.save(filepath)
    r = translate.client.asr(get_file_content(filepath), 'pcm')
    return r


@app.route('/getaudioen', methods=['POST'])
def getaudioen():
    translator_selector = request.form["translator_selector"]
    audiofile = request.files.get("audioData")
    if audiofile:
        filepath = "audio/%s.pcm" % uuid.uuid4()
        audiofile.save(filepath)
    r = translate.client.asr(get_file_content(filepath), 'pcm',16000,{
    'dev_pid': 1737,
})
    print(r)
    if(translator_selector=='Baidu'):
        t=translate.trans_baidu(''.join(r['result']), 'en', 'zh')
    if(translator_selector=='Youdao'):
        t=translate.trans_youdao(''.join(r['result']), 'en', 'zh-CHS')
    if(translator_selector=='Google'):
        t=translate.trans_google(''.join(r['result']), 'en', 'zh-cn')
    return t


@app.route('/getaudiozh', methods=['POST'])
def getaudiozh():
    translator_selector = request.form["translator_selector"]
    audiofile = request.files.get("audioData")
    if audiofile:
        filepath = "audio/%s.pcm" % uuid.uuid4()
        audiofile.save(filepath)
    r = translate.client.asr(get_file_content(filepath), 'pcm',16000,{
    'dev_pid': 1537,
})
    if(translator_selector=='Baidu'):
        t=translate.trans_baidu(''.join(r['result']), 'zh', 'en')
    if(translator_selector=='Youdao'):
        t=translate.trans_youdao(''.join(r['result']), 'zh-CHS', 'en')
    if(translator_selector=='Google'):
        t=translate.trans_google(''.join(r['result']), 'zh-cn', 'en')
    return t

def is_contain_chinese(check_str):
    """
    判断字符串中是否包含中文
    :param check_str: {str} 需要检测的字符串
    :return: {bool} 包含返回True， 不包含返回False
    """
    for ch in check_str:
        if u'\u4e00' <= ch <= u'\u9fff':
            return True
    return False


@app.route('/getstr', methods=['POST'])
def getstr():
    translator_selector = request.form["translator_selector"]
    r=request.form["text"]
    if(is_contain_chinese(r)):
        if(translator_selector=='Baidu'):
            t=translate.trans_baidu(r, 'zh', 'en')
        if(translator_selector=='Youdao'):
            t=translate.trans_youdao(r, 'zh-CHS', 'en')
        if(translator_selector=='Google'):
            t=translate.trans_google(r, 'zh-cn', 'en')
    else:
        if(translator_selector=='Baidu'):
            t=translate.trans_baidu(r, 'en', 'zh')
        if(translator_selector=='Youdao'):
            t=translate.trans_youdao(r, 'en', 'zh-CHS')
        if(translator_selector=='Google'):
            t=translate.trans_google(r, 'en', 'zh-cn') 
    return t

if __name__ == '__main__':
    app.run(debug=True)
