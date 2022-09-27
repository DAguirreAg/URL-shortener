from fastapi import FastAPI, Path, Depends, HTTPException, Response, responses
from sqlalchemy.orm import Session
from starlette.requests import Request
import starlette.status as status
import uvicorn
from sql_app import crud, models, schemas
from sql_app.database import SessionLocal, engine
from utils import idToShortURL, shortURLToId
import validators
from config import Config

# Main App
app = FastAPI(
    title=Config.TITLE,
    description=Config.DESCRIPTION,
    version=Config.VERSION,
    contact=Config.CONTACT,
    license_info=Config.LICENSE_INFO,
    openapi_tags=Config.TAGS_METADATA
)

models.Base.metadata.create_all(bind=engine)

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/{shortURL}", tags=['Urls'])
def get_longURL(shortURL: str, request: Request, db: Session = Depends(get_db)):
    '''Logic to get longURL from shortURL'''

    # Get id from shortURL
    id = shortURLToId(shortURL)

    # Fetch data
    longURL = crud.get_longURL(db, id=id)

    if longURL is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="LongURL not found")

    # Register visit
    crud.create_transaction(db, shortURL, request.headers)

    return responses.RedirectResponse(url=longURL, status_code=status.HTTP_307_TEMPORARY_REDIRECT)


@app.post("/create-shortURL", tags=['Urls'])
def create_shortURL(longURL: str, db: Session = Depends(get_db)):
    '''Logic to create a shortURL based on longURL'''

    # Validate LongURL
    if not validators.url(longURL):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Provided URL not correct.")
    
    # Check if LongURL in DB
    if crud.check_longURL_in_db(db, longURL):
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="LongURL already exists")

    # Get unique ID and calculate shortURL
    nextID = crud.get_next_id(db)
    shortURL = idToShortURL(nextID)

    # Add to DB
    crud.create_shortURL(db, nextID, shortURL, longURL)

    return {"shortURL": shortURL}
    

@app.delete("/delete-shortURL", tags=['Urls'])
def delete_shortURL(shortURL: str, db: Session = Depends(get_db)):
    crud.delete_shortURL(db, shortURL)
    return {}

if __name__ == "__main__":
    uvicorn.run(app, port=1234, host='0.0.0.0')