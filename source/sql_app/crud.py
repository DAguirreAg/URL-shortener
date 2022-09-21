from urllib import request
from sqlalchemy.orm import Session
from . import models, schemas
from starlette.requests import Request

def get_longURL(db: Session, id: int):
    results = db.query(models.Urls).filter(models.Urls.id == id).first() 

    if results is None:
        return None
    
    longURL = results.longURL
    return longURL

def create_transaction(db: Session, shortURL: str, headers: Request.headers): 
    transaction = models.Transactions(shortURL=shortURL, header=headers)
    db.add(transaction)
    db.commit()

def check_longURL_in_db(db: Session, longURL: str):
    results = db.query(models.Urls).filter(models.Urls.longURL == longURL).first()
    return results

def create_shortURL(db: Session, id: int, shortURL: str, longURL: str):
    url = models.Urls(id=id, shortURL=shortURL, longURL=longURL)
    db.add(url)
    db.commit()

def delete_shortURL(db: Session, shortURL: str):
    db.query(models.Urls).filter(models.Urls.shortURL==shortURL).delete()
    db.commit()

def get_next_id(db: Session):
    nextID = models.seq_obj.execute()
    return nextID