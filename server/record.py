from sqlalchemy import Column, String, Integer
from sqlalchemy.ext.declarative import declarative_base
from db import dbEngine, db_session

def init_db():
    Model.metadata.create_all(bind=dbEngine)

Model = declarative_base(name='Model')
Model.query = db_session.query_property()

class RenderList(Model):
    __tablename__ = 'render_lists'
    position = Column('position', Integer, primary_key=True)
    title = Column('title', String)
    type = Column('type', String)
    link = Column('link', String)

    def __init__(self, title, type, link):
        self.title = title
        self.type = type
        self.link = link
    
    def to_dictionary(self):
        return { 'position': self.position, 'title': self.title, 'type': self.type, 'link': self.link }
