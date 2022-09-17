from fastapi import FastAPI, Path
from utils import idToShortURL, shortURLToId
from models import getLongURL, checkShortURLinDB, checkLongURLinDB, insertShortURL, logTranscation
from starlette.requests import Request
from IDGenerator import IDGenerator

app = FastAPI()
idgenerator = IDGenerator()

@app.get("/{shortURL}")
def get_longURL(shortURL: str, request: Request):
    '''Logic to get longURL from shortURL'''

    # Get id from shortURL
    id = shortURLToId(shortURL)

    # Get longURL from id.
    longURL = getLongURL(id)

    # Register visit
    logTranscation(shortURL, request.headers)
        
    return longURL
    

@app.post("/create-shortURL/")
def create_shortURL(longURL: str):
    '''Logic to create a shortURL based on longURL'''

    # Check if shortURL in DB
    if checkLongURLinDB(longURL):
        return {'error' : 'url already exists'}
    
    # Get unique ID and calculate shortURL
    id = idgenerator.getNextID()
    shortURL = idToShortURL(id)

    # Add to DB
    insertShortURL(id, shortURL, longURL)
    
    return shortURL

