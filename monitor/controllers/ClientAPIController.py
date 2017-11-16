#coding:utf8
from flask import Blueprint, request, render_template, flash, g, session, redirect, url_for, jsonify
import json

from monitor.repositories.repository import write_db, read_db_server_within, read_db_service_within
from monitor.config import config

client_api = Blueprint('client_api', __name__)

@client_api.route("/api/get_server_data/<servername>/<hours>")
def get_server_data(servername, hours):
    '''
    for echart rendering
    '''
    result_sample = {
        'local':[123.11, 234.22, 345.33],
        'cat':[222.22, 333.33, 444.44]
    }
    result = {}
    data = read_db_server_within(servername, int(hours))
    for i in data:
        if i.agent in result:
            result[i.agent]['date'].append(str(i.time))
            result[i.agent]['data'].append(i.ping)
        else:
            result[i.agent] = {
                'date':[],
                'data':[]
            }
            print i.time
            result[i.agent]['date'].append(str(i.time))
            result[i.agent]['data'].append(i.ping)
    return jsonify(result)

@client_api.route("/api/get_service_from_server/<servername>")
def get_service_from_server(servername):
    '''获取某一服务器的所有服务'''
    result = []
    for server in config['servers']:
        if server['name'] == servername:
            for service in server['services']:
                result.append(service['name'])
    return jsonify(result)

@client_api.route("/api/get_service_data/<servicename>/<hours>")
def get_service_data(servicename, hours):
    '''
    for echart rendering
    '''
    result = {}
    data = read_db_service_within(servicename, int(hours))
    time = []
    data_list = []
    for i in data:
        time.append(str(i.time))

    for i in range(0,2):
        for j in range(0,len(data)-1):
            if i == 0:
                data_list.append([i,j,data[j].http])
            elif i == 1:
                data_list.append([i,j,data[j].https])

    result = {
        'name':data[0].name,
        'server':data[0].server_name,
        'url':data[0].url,
        'time':time,
        'agent':data[0].agent,
        'data':data_list
    }
    return jsonify(result)