from fastapi import FastAPI, Path, Depends, HTTPException
from sqlalchemy.orm import Session
from starlette.requests import Request
from utils import idToShortURL, shortURLToId
from IDGenerator import IDGenerator

from sql_app import crud, models, schemas
from sql_app.database import SessionLocal, engine

app = FastAPI()
models.Base.metadata.create_all(bind=engine)
idgenerator = IDGenerator()

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/{shortURL}", response_model=schemas.LongUrl)
def get_longURL(shortURL: str, request: Request, db: Session = Depends(get_db)):
    '''Logic to get longURL from shortURL'''
    # Get id from shortURL
    id = shortURLToId(shortURL)

    # Fetch data
    longURL = crud.get_longURL(db, id=id)

    if longURL is None:
        raise HTTPException(status_code=404, detail="LongURL not found")

    # Register visit
    crud.create_transaction(db, shortURL, request.headers)

    return longURL


@app.post("/create-shortURL/")
def create_shortURL(longURL: str, db: Session = Depends(get_db)):
    '''Logic to create a shortURL based on longURL'''

    # Check if shortURL in DB
    if crud.check_longURL_in_db(db, longURL):
        raise HTTPException(status_code=404, detail="LongURL already exists")

    # Get unique ID and calculate shortURL
    id = idgenerator.getNextID()
    shortURL = idToShortURL(id)

    # Add to DB
    crud.create_shortURL(db, id, shortURL, longURL)
    
    return shortURL

