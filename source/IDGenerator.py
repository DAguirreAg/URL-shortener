class IDGenerator:
    
    latest_id = 570
    
    def __init__(self):
        pass       
    
    def getNextID(self):
        IDGenerator.latest_id += 1
        return IDGenerator.latest_id
