from sqlalchemy import create_engine, Table, Column, Integer, String, DateTime, MetaData, ForeignKey
from sqlalchemy.sql import func
import sqlalchemy

# Settings
db_uri = "sqlite:///urlShortener.db"

engine = create_engine(db_uri, echo = True)
meta = MetaData()

## Table definitions
urls = Table(
    'urls', meta, 
    Column('id', Integer, primary_key = True), 
    Column('shortURL', String), 
    Column('longURL', String), 
)

transactions = Table(
    'transactions', meta, 
    Column('id', Integer, primary_key = True), 
    Column('shortURL', String, ForeignKey('urls.shortURL', ondelete='CASCADE')), 
    Column('time_created', DateTime(timezone=True), server_default=func.now()),
    Column('header', String)
)


## DB functions
def getLongURL(id):

    query = sqlalchemy.select(urls).where(urls.c.id == id)    
    result = engine.execute(query).first()
    
    if result:
        return result['longURL']
        
    return None

def checkShortURLinDB(shortURL):
    
    query = sqlalchemy.select(urls).where(urls.c.shortURL == shortURL)    
    result = engine.execute(query).first()
    
    if result:
        return True
    
    return False

def checkLongURLinDB(longURL):
    
    query = sqlalchemy.select(urls).where(urls.c.longURL == longURL)    
    result = engine.execute(query).first()
    
    if result:
        return True
    
    return False

def insertShortURL(id, shortURL, longURL):

    url = urls.insert().values(id=id, shortURL=shortURL, longURL=longURL)
    conn = engine.connect()
    result = conn.execute(url)


def logTranscation(shortURL, headers):

    headers = str(headers)
    transaction = transactions.insert().values(shortURL=shortURL, header=headers)
    conn = engine.connect()
    result = conn.execute(transaction)
