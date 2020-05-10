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
    r = translate.client.asr(get_file_content(filepath), 'pcm')
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
    r = translate.client.asr(get_file_content(filepath), 'pcm')
    if(translator_selector=='Baidu'):
        t=translate.trans_baidu(''.join(r['result']), 'zh', 'en')
    if(translator_selector=='Youdao'):
        t=translate.trans_youdao(''.join(r['result']), 'zh-CHS', 'en')
    if(translator_selector=='Google'):
        t=translate.trans_google(''.join(r['result']), 'zh-cn', 'en')
    return t


if __name__ == '__main__':
    app.run(debug=True)
