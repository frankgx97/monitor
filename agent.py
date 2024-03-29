# coding:utf8

import json

import pyping
import requests


class MonitorInstance():

    config = {}

    def __init__(self, config):
        self.config = config

    def get_status(self, ping):
        if ping != -1:
            if ping > 300:
                return 'unstable'
            else:
                return 'online'
        else:
            return 'offline'

    def get_ping(self):
        counter = 0
        while counter < 3:
            ping_rst = self.do_ping()
            counter += 1
            if ping_rst <= 600 and ping_rst > 0:
                break
        return ping_rst

    def do_ping(self):
        if self.config['ping']:
            try:
                r = pyping.ping(self.config['server'])
                if r.ret_code is 1:
                    return -1
                else:
                    return r.avg_rtt
            except:
                return -1
        else:
            return False

    def get_http_result(self, url, config):
        if not config['enable']:
            return 'disabled'
        splitted_url = url.split('://', 1)
        if config['port'] == 80:
            url = 'http://' + splitted_url[1]
        elif config['port'] == 443:
            url = 'https://' + splitted_url[1]
        try:
            status_code = requests.get(url).status_code
        except:
            return 'offline'
        if status_code in config['expect']:
            return 'online'
        else:
            return 'error'

    def get_result(self):
        result = {}
        result['server'] = self.config['server']
        result['name'] = self.config['name']
        result['ping'] = float(self.get_ping())
        result['status'] = self.get_status(result['ping'])
        result['services'] = []
        for service in self.config['services']:
            service_result = {
                'name': service['name'],
                'url': service['url'],
                'http': self.get_http_result(service['url'], service['http']),
                'https': self.get_http_result(service['url'], service['https'])
            }
            result['services'].append(service_result)

        print result
        return result


def monitor():
    result = []
    config = json.loads(open('./agent_config.json').read())
    r = requests.post(config['master_url'] + 'api/get_server_list', json={
        'agent_name':config['agent_name'],
        'agent_key': config['agent_key']
    })
    #print r.content
    #if json.loads(r.content)['status'] != 0:
    #    raise Exception(json.loads(r.content)['error'])
    for server in json.loads(r.content):
        server_instance = MonitorInstance(server)
        result.append(server_instance.get_result())
    return result


def send_result(result):
    '''将检测结果发送给master'''
    config = json.loads(open('agent_config.json').read())
    requests.post(config['master_url'] + 'api/add_record', json={
        'agent_name':config['agent_name'],
        'agent_key': config['agent_key'],
        'servers':result
    })

rst = monitor()
send_result(rst)
