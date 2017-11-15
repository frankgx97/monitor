#coding:utf8
from flask import Blueprint, request, render_template, flash, g, session, redirect, url_for, jsonify
import json

from monitor.repositories.repository import write_db
from monitor.config import config

agent_api = Blueprint('agent_api', __name__)

@agent_api.route("/api/get_server_list", methods=['POST'])
def get_server_list():
    '''从master获得需要监控的服务器和服务列表'''
    data = request.get_json()
    if not verify_agent(data):
        return jsonify({'status':1, 'error':'AccessDenied'})
    #config = json.loads(open('master_config.json').read())
    #config = app.config['configure']
    return jsonify(config['servers'])

def verify_agent(data):
    '''验证agent的key是否正确'''
    print data
    #config = json.loads(open('master_config.json').read())
    agent_name = data['agent_name']
    agent_key = data['agent_key']
    for i in config['agents']:
        if i['name'] == agent_name and i['key'] == agent_key:
            return True
    return False

@agent_api.route("/api/add_record", methods=['POST'])
def add_record():
    '''添加一条新纪录'''
    data = request.get_json()
    if not verify_agent(data):
        return jsonify({'status':1, 'error':'AccessDenied'})
    #写数据库
    write_db(data)
    #TODO:报警
    return jsonify({'status':0, 'error':'success'})