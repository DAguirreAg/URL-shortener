# URL-shortener
The following repository contains code as a proof of concept of a URL shortener application.

The main task of URL shorteners is to take long strings of URLs and convert them into shorter ones. They have the advantage that they can be pasted in character limited text fields (twitter, messaging boards, ...) as well as they are able to register visitors information such as time of login and the device they logged from.

<p align="middle">
  <img src="documentation/URL-Shortener%20Main%20page.png" alt="URL-Shortener Main page.png" height=500></br>
  <i>URL-Shortener Main page.png</i>
</p>

## 1. How to use it
Follow the next steps:
* Open the `config.py` file and modify the `SQLALCHEMY_DATABASE_URL` to your favourite database. (Please note that due to the usage of Sequences for ID generation, SQLite cannot be used).
* Install the required python packages via `pip install -r requirements.txt`. (It is recommended to use virtual environments when installing them to avoid conflicting version issues).
* Open a terminal window and type `uvicorn main:app --reload` to launch the application.
* Open a browser and type `http://127.0.0.1:800/docs` in the address bar to open an interactive view of the App.

<p align="middle">
  <img src="documentation/Running%20URL-shortener%20App.png" alt="Running URL-shortener App.png" height=200></br>
  <i>Running URL-shortener App</i>
</p>

## 2. Technical details

### 2.1. System design
The App consists of three main endpoints:
* Create shortURL: Creates a "random" shortURL and asigns it to the longURL as long as the longURL hasn't been used before. 
* Retrieve longURL: It redirects any user that uses the link to the longURL associated with that shortURL. It also logs information about the user who requested that longURL
* Delete shortURL: It deletes the shortURL as well as the related transactions/logs.

<p align="middle">
  <img src="documentation/Process%20diagram%20for%20creating%20a%20ShortURL.png" alt="Process diagram for creating a ShortURL.png" height=200>
  <img src="documentation/Process%20diagram%20for%20retrieving%20the%20LongURL.png" alt="Process diagram for retrieving the LongURL.png" height=200>
  <img src="documentation/Process%20diagram%20for%20deleting%20a%20ShortURL.png" alt="Process diagram for deleting a ShortURL.png" height=200>
  </br>
  <i>Main endpoints of the script</i>
</p>

### 2.2. Theory on URL shortening
Because the idea of URL-shortening services is to provide a shortURL that always points to the same longURL, one of the best choices is to use the 26 alphanumeric characters and the number digits. This gives 62 possible combinations per character: 26 lowercase alphanumeric characters [a-z] + 26 uppercase alphanumeric characters [A-Z] + 10 numerical digits [0-9].

With this in mind, we can create **a function in base 62** that converts a string of characters+numbers into integer numbers and vice versa.  Below snippet shows a simple way of converting an integer number into the corresponding 62 base string and vice versa. Note that one of the main issues is about how you make the initial ID generation highly available and at the same time you ensure no duplicates are generated (as a shortURL should always point to the same longURL). Check [this page](https://www.geeksforgeeks.org/system-design-url-shortening-service/) for interesting discussion regarding pros/cons on different approaches.

```
## URL shortener functions
def find(n, m):
     
    # Quotient
    q = n//m
     
    # Remainder
    r = n%m
    
    return q, r

def idToShortURL(id):
    
    map = '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'

    # Get Hashvalue from ID
    shortURL = ''
    quotient = id
    while quotient >= 62:
        quotient, remainder = find(quotient, 62)
        shortURL += map[remainder]
    shortURL += map[quotient]
    
    return shortURL[len(shortURL): : -1]


def shortURLToId(shortURL):
    
    map = '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
    
    # Get ID from Hashvalue
    result = 0
    i = -1
    for c in shortURL[len(shortURL): : -1]:
        i += 1
        result += pow(62, i) * map.find(c)
        
    return result
```

## 3. Future functionalities/Considerations
As a proof of concept of a URL shortener application, the source code doesn't implement all the functionalities that a proper URL shortener should have. On the one hand, as a simple SQL database is used for storing URLs and generating the IDs, it becomes a single point of failure and it makes the scalability extremelly difficult. On the other hand, the lack of user authentification and account creation, makes anybody be able to delete/create shortURLs possible. 

Because of this, below there is a list of all the functionalities that will need to be considered implemented in the current repository to make it fully functional:
* Add user authentication for URL management.
* Add scalability and availability. The current design contains a single point of failure (the database), which if it goes down, it will halt the full retrieval of the LongURLs (and creation of new ones).
* Check for security vulnerabilities. (Note that even though an ORM is used, an investigation should be carried out to discard XSS and SQL injection vulnerabilities).
* Implement proper configuration.
* Implement unit testing and create a testing DB connection.
* Enable Async functionality.

## 4. Disclaimers
This is a proof of concept project that aims to shown how a URL shortening service works. Bear in mind, that as many POC, it is not a final product and many points need to be considered before making the code production ready.


## References
* [System Design Interview Volume 1](https://blog.bytebytego.com/p/system-design-interview-books-volume)
* [URL shortener](https://www.geeksforgeeks.org/system-design-url-shortening-service/)
