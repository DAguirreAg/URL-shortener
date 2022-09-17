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

