#coding:utf8
from flask import Blueprint, render_template
#from monitor import app
from monitor.repositories.repository import get_server_result_latest, read_db_server_within, read_db_service_within
from monitor.config import config

web_module = Blueprint('web_module', __name__)

@web_module.route("/")
def index():
    '''渲染首页HTML模板'''
    result = []
    for server in config['servers']:
        result.append(get_server_result_latest(server))
    return render_template('index.html', result=result, server_list=result)

@web_module.route("/server/<servername>")
def get_server(servername):
    '''渲染首页HTML模板'''
    result = {}
    result['services'] = []
    result['servers'] = read_db_server_within(servername, 24)
    for server in config['servers']:
        if server['name'] == servername:
            for service in server['services']:
                result['services'].append(read_db_service_within(service['name'], 24))
            break
    server_list = []
    for server in config['servers']:
        server_list.append(get_server_result_latest(server))
    return render_template('server.html', result=result, server_list=server_list)