# coding:utf8

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import json

from monitor.config import config

#db_config = json.loads(open("master_config.json").read())['mysql']
db_config = config['mysql']
db_connection = "mysql+mysqldb://"+db_config['user']+":"+db_config['password']+"@"+db_config['host']+":"+str(db_config['port'])+"/"+db_config['db']

engine = create_engine(db_connection, convert_unicode=True)
db_session = scoped_session(
    sessionmaker(autocommit=False,
                 autoflush=False,
                 bind=engine)
)
Base = declarative_base()
Base.query = db_session.query_property()


def init_db():
    # import all modules here that might define models so that
    # they will be registered properly on the metadata.  Otherwise
    # you will have to import them first before calling init_db()
    import models
    Base.metadata.create_all(bind=engine)
