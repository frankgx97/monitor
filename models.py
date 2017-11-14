#coding:utf8

from sqlalchemy import Column, Integer, String, Float, DateTime, func
from database import Base

class Service(Base):
    __tablename__ = 'services'
    id = Column(Integer, primary_key=True)
    server_name = Column(String(50))
    name = Column(String(50))
    agent = Column(String(50))
    url = Column(String(50))
    http = Column(Integer) # 0=off, 1=on, -1=disable
    https = Column(Integer)
    time = Column(DateTime(timezone=True), server_default=func.now())

    def __init__(self, server_name, name, agent, url, http, https):
        self.server_name = server_name
        self.name = name
        self.agent = agent
        self.url = url
        self.http = http
        self.https = https

    def __repr__(self):
        return '<Service %r>' % (self.name)

class Server(Base):
    __tablename__ = 'servers'
    id = Column(Integer, primary_key=True)
    name = Column(String(50))
    agent = Column(String(50))
    server = Column(String(50))
    status = Column(Integer)#0=off,1=on,2=unstable
    ping = Column(Float)
    time = Column(DateTime(timezone=True), server_default=func.now())

    def __init__(self, name, server, agent, status, ping):
        self.server = server
        self.name = name
        self.agent = agent
        self.status = status
        self.ping = ping

    def __repr__(self):
        return '<Server %r>' % (self.name)
