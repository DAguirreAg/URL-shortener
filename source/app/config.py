

class Config:
    
    # DB settings
    SQLALCHEMY_DATABASE_URL = 'postgresql+psycopg2://postgres:mysecretpassword@localhost:5432/urlShortener_app'

    # App settings
    ## Metadata 
    DESCRIPTION = '''
    URL-Shortener App is a simplified implementation of common URL-shortener services as [TinyURL](https://tinyurl.com/app) or [Bit.ly](https://bitly.com/).
    '''

    TAGS_METADATA = [
        {
            "name": "Urls",
            "description": "Operations with Urls. Includes the creation of shortURLs and retrieval of the longURLs.",
        }
    ]

    TITLE="URL-Shortener App"
    VERSION="0.0.1"
    CONTACT={
            "name": "DAguirreAg",
            "url": "https://github.com/DAguirreAg/"
            }
    LICENSE_INFO={
                "name": " MIT License",
                "url": "https://mit-license.org/",
                }