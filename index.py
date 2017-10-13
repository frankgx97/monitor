#coding:utf8
from flask import Flask, render_template, request
from flask import jsonify
import json
from database import db_session
from models import Server, Service

app = Flask(__name__, static_url_path='/static')  # 定义/static目录为静态文件目录

#模板
@app.route("/")
def index():
    '''渲染首页HTML模板'''
    return render_template('index.html')

@app.route("/server")
def server():
    '''渲染首页HTML模板'''
    return render_template('server.html')

#API
@app.route("/api/add_record", methods=['POST'])
def add_record():
    '''添加一条新纪录'''
    data = request.get_json()
    if not verify_agent(data):
        return jsonify({'status':1, 'error':'AccessDenied'})
    #写数据库
    write_db(data)
    #报警
    return jsonify({'status':0, 'error':'success'})

@app.route("/api/get_server_list")
def get_server_list():
    '''从master获得需要监控的服务器和服务列表'''
    config = json.loads(open('master_config.json').read())
    return jsonify(config['servers'])

#函数

@app.teardown_appcontext
def shutdown_session(exception=None):
    db_session.remove()


def write_db(data):
    for server in data['servers']:
        s = Server(
            server['name'],
            server['server'],
            convert_status(server['status']),
            server['ping']
            )
        db_session.add(s)
        db_session.commit()
        for service in server['services']:
            srv = Service(
                server['name'],
                service['name'],
                service['url'],
                convert_status(service['http']),
                convert_status(service['https'])
                )
            db_session.add(srv)
            db_session.commit()

def convert_status(st):
    if st is 'online':
        return 1
    elif st is 'offline':
        return 0
    elif st is 'disable':
        return -1
    else:
        return 2

def verify_agent(data):
    '''验证agent的key是否正确'''
    config = json.loads(open('master_config.json').read())
    agent_name = data['agent_name']
    agent_key = data['agent_key']
    for i in config['agents']:
        if i['name'] == agent_name and i['key'] == agent_key:
            return True
    return False
