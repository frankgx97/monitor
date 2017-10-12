#coding:utf8
from flask import Flask, render_template, request
from flask import jsonify
import json

app = Flask(__name__, static_url_path='/static')  # 定义/static目录为静态文件目录

@app.route("/")
def index():
    '''渲染首页HTML模板'''
    return render_template('index.html')

@app.route("/add_record")
def add_record():
    '''添加一条新纪录'''
    data = request.args.get("data")
    data = json.loads(data)
    if not verify_agent(data):
        return jsonify({'status':1, 'error':'AccessDenied'})
    #写数据库
    #报警
    return jsonify({'status':0, 'error':'success'})


def verify_agent(data):
    config = json.loads(open('master_config.json').read())
    agent_name = data['agent_name']
    agent_key = data['agent_key']
    for i in config['agents']:
        if (i['name'] is agent_name) and (i['key'] is agent_key):
            return True
    return False
