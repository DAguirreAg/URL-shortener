from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.sql import func
from .database import Base

class Urls(Base):
    __tablename__ = 'urls'

    id = Column(Integer, primary_key = True, index=True)
    shortURL = Column(String)
    longURL = Column(String)

class Transactions(Base):
    __tablename__ = 'transactions'

    id = Column(Integer, primary_key = True, index=True)
    shortURL = Column(String, ForeignKey('urls.shortURL', ondelete='CASCADE'))
    time_created = Column(DateTime(timezone=True), server_default=func.now())
    header = Column(String)
