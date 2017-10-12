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
        if self.config['ping']:
            r = pyping.ping(self.config['server'])
            if r.ret_code is 1:
                return -1
            return r.avg_rtt
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
    config = json.loads(open('config.json').read())
    for server in config['servers']:
        server_instance = MonitorInstance(server)
        result.append(server_instance.get_result())
    return result


def send_result(result):
    result_json = json.dumps(result)
    requests.post(
        'http://xxx.xxx',
        result_json
    )

rst = monitor()
#send_result(rst)
