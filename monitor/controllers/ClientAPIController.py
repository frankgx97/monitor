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
