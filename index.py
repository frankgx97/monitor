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
    result = []
    config = json.loads(open('master_config.json').read())
    for server in config['servers']:
        result.append(get_server_result(server))
    print result
    return render_template('index.html', result=result)

@app.route("/server/<servername>")
def get_server(servername):
    '''渲染首页HTML模板'''
    config = json.loads(open('master_config.json').read())
    for server in config['servers']:
        if server['name'] == servername:
            result = get_server_result(server)
            break
    return render_template('server.html', result=result)

#API
@app.route("/api/add_record", methods=['POST'])
def add_record():
    '''添加一条新纪录'''
    data = request.get_json()
    if not verify_agent(data):
        return jsonify({'status':1, 'error':'AccessDenied'})
    #写数据库
    write_db(data)
    #TODO:报警
    return jsonify({'status':0, 'error':'success'})

@app.route("/api/get_server_list", methods=['POST'])
def get_server_list():
    '''从master获得需要监控的服务器和服务列表'''
    data = request.get_json()
    if not verify_agent(data):
        return jsonify({'status':1, 'error':'AccessDenied'})
    config = json.loads(open('master_config.json').read())
    return jsonify(config['servers'])

#函数
@app.teardown_appcontext
def shutdown_session(exception=None):
    db_session.remove()

def get_server_result(server):
    server_result = {}
    server_result_db_read = read_db_server_latest(server['name'])
    server_result['name'] = server_result_db_read.name
    server_result['server'] = server_result_db_read.server
    server_result['status'] = server_result_db_read.status
    server_result['ping'] = server_result_db_read.ping
    server_result['services'] = []
    for service in server['services']:
        service_result = {}
        service_result_db_read = read_db_service_latest(service['name'])
        service_result['name'] = service_result_db_read.name
        service_result['url'] = service_result_db_read.url
        service_result['http'] = service_result_db_read.http
        service_result['https'] = service_result_db_read.https
        server_result['services'].append(service_result)
    return server_result

def read_db_server_latest(server_name):
    '''读取指定服务器的最新一条监控记录'''
    return list(reversed(Server.query.filter(Server.name == server_name).all()))[0]

def read_db_service_latest(service_name):
    '''读取指定服务的最新一条监控记录'''
    return list(reversed(Service.query.filter(Service.name == service_name).all()))[0]

def write_db(data):
    for server in data['servers']:
        s = Server(
            server['name'],
            data['agent_name'],
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
                data['agent_name'],
                service['url'],
                convert_status(service['http']),
                convert_status(service['https'])
                )
            db_session.add(srv)
            db_session.commit()

def convert_status(st):
    if st == 'online':
        return 1
    elif st == 'offline':
        return 0
    elif st == 'disable':
        return -1
    else:
        return 2

def verify_agent(data):
    '''验证agent的key是否正确'''
    print data
    config = json.loads(open('master_config.json').read())
    agent_name = data['agent_name']
    agent_key = data['agent_key']
    for i in config['agents']:
        if i['name'] == agent_name and i['key'] == agent_key:
            return True
    return False
