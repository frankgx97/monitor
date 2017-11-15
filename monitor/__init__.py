#coding:utf8
from flask import Flask, current_app, render_template, request

from .controllers.AgentAPIController import agent_api
from .controllers.WebController import web_module

app = Flask(__name__, static_url_path='/static')  # 定义/static目录为静态文件目录
#app.config.from_pyfile('../config.py')

#config = json.loads(open("master_config.json").read())


app.register_blueprint(agent_api)
app.register_blueprint(web_module)
