from sqlalchemy import Column, Integer, String, Text, Date
from model.database  import Base
from datetime import date
import datetime

class main(Base):
    __tablename__ = 'main'
    id = Column(Integer, primary_key=True)
    title = Column(String(128),)
    date = Column(Date, default=date.today())
    deadline = Column(String(10),)

    def __init__(self, title=None, date=None,deadline=None):
        self.title = title
        self.date = date
        self.deadline = deadline

    def __repr__(self):
        return '<Title %r>' % (self.title)

