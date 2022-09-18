from typing import List, Union

from pydantic import BaseModel

class UrlBase(BaseModel):
    pass


class LongUrl(UrlBase):

    longURL: str
    
    class Config:
        orm_mode = True

class ShortUrl(UrlBase):

    shortUrl: str
    
    class Config:
        orm_mode = True