#coding:utf8

from sqlalchemy import Column, Integer, String
from database import Base

class Record(Base):
    __tablename__ = 'records'
    id = Column(Integer, primary_key=True)
    content = Column(String())

    def __init__(self, content=None):
        self.content = content

    def __repr__(self):
        return '<User %r>' % (self.content)
