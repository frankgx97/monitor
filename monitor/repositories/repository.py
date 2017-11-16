#coding:utf8
#from monitor import app
from monitor.db.database import db_session
from monitor.db.models import Server, Service
import datetime

'''
@app.teardown_appcontext
def shutdown_session(exception=None):
    db_session.remove()
'''

def get_server_result_latest(server):
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

def read_db_server_within(server_name, hours):
    '''读取指定服务器的特定时间范围内监控记录'''
    current_time = datetime.datetime.now()
    one_day_ago = current_time - datetime.timedelta(hours=hours)
    return list(reversed(Server.query.filter(Server.name == server_name, Server.time > one_day_ago).all()))

def read_db_service_within(service_name, hours):
    '''读取指定服务器的特定时间范围内监控记录'''
    current_time = datetime.datetime.now()
    one_day_ago = current_time - datetime.timedelta(hours=hours)
    return list(reversed(Service.query.filter(Service.name == service_name, Service.time > one_day_ago).all()))

def write_db(data):
    for server in data['servers']:
        s = Server(
            server['name'],
            server['server'],
            data['agent_name'],
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
    elif st == 'disabled':
        return -1
    else:
        return 2
