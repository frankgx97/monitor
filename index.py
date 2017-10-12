#coding:utf8
from flask import Flask, render_template, request
from flask import jsonify
import json

app = Flask(__name__, static_url_path='/static')  # 定义/static目录为静态文件目录

@app.route("/")
def index():
    '''渲染首页HTML模板'''
    return render_template('index.html')

@app.route("/gettext")
def gettextapi():
    '''获得正文抽取的接口，返回status和result'''
    url = request.args.get("url")
    result = json.dumps({'status': 0, 'result': cx.get_text_from_url(url)})
    return result