#coding:utf8
from flask import Flask, render_template, request, current_app
from flask import jsonify
import datetime

#Blueprints

from monitor import app

#app = Flask(__name__, static_url_path='/static')  # 定义/static目录为静态文件目录
#app.config.from_pyfile('config.py')

#Register blueprints

#模板


@app.route("/test")
def test():
    print read_db_server_within('cat', 24)

#ClientAPI


#AgentAPI

#函数

