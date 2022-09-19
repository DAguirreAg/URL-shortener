from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Sequence, MetaData
from sqlalchemy.sql import func
from .database import Base, engine

# Create Sequence
metadata = MetaData(bind=engine)
seq_obj = Sequence('urls_id_seq', metadata=metadata)

class Urls(Base):
    __tablename__ = 'urls'

    id = Column(Integer, primary_key = True, index=True, unique=True)
    shortURL = Column(String, unique=True)
    longURL = Column(String)

class Transactions(Base):
    __tablename__ = 'transactions'

    id = Column(Integer, primary_key = True, index=True, unique=True)
    shortURL = Column(String, ForeignKey('urls.shortURL', ondelete='CASCADE'))
    time_created = Column(DateTime(timezone=True), server_default=func.now())
    header = Column(String)
